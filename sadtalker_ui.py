import os
import sys
import subprocess
import threading
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox, 
                            QProgressBar, QTextEdit, QFileDialog, QMessageBox, QGroupBox,
                            QFrame)
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from PyQt5.QtGui import QFont, QColor, QPalette

class ProcessThread(QThread):
    output_received = pyqtSignal(str)
    process_finished = pyqtSignal(int)
    video_path_found = pyqtSignal(str)
    
    def __init__(self, command):
        super().__init__()
        self.command = command
        
    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Process output in real-time
            for line in iter(process.stdout.readline, ''):
                self.output_received.emit(line.strip())
                if "The generated video is named" in line and ".mp4" in line:
                    try:
                        # Extract the video path from the output
                        video_path = line.split("named")[1].strip()
                        if video_path.startswith(":"):
                            video_path = video_path[1:].strip()
                        self.video_path_found.emit(video_path)
                    except:
                        pass
            
            process.stdout.close()
            return_code = process.wait()
            self.process_finished.emit(return_code)
                
        except Exception as e:
            self.output_received.emit(f"Error occurred: {str(e)}")
            self.process_finished.emit(1)

class SadTalkerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SadTalker - AI Talking Face Generator")
        self.setMinimumSize(800, 700)
        
        # Instance variables
        self.source_image_path = ""
        self.audio_path = ""
        self.result_path = ""
        self.process_thread = None
        
        # Setup UI
        self.init_ui()
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        
        # Title
        title_label = QLabel("SadTalker UI")
        title_font = QFont("Arial", 16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Generate talking face videos from images and audio")
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)
        
        # Source image selection - in a frame with border
        image_frame = QFrame()
        image_frame.setFrameShape(QFrame.StyledPanel)
        image_frame.setLineWidth(1)
        image_layout = QVBoxLayout(image_frame)
        
        image_header = QLabel("📷 SOURCE IMAGE")
        image_header.setStyleSheet("font-weight: bold; font-size: 14px;")
        image_layout.addWidget(image_header)
        
        image_desc = QLabel("Select an image containing a face (portrait or full body)")
        image_layout.addWidget(image_desc)
        
        image_input_layout = QHBoxLayout()
        self.image_path_edit = QLineEdit()
        self.image_path_edit.setReadOnly(True)
        self.image_path_edit.setPlaceholderText("No image selected")
        
        browse_image_btn = QPushButton("Browse for Image...")
        browse_image_btn.setMinimumWidth(150)
        browse_image_btn.clicked.connect(self.browse_image)
        
        image_input_layout.addWidget(self.image_path_edit)
        image_input_layout.addWidget(browse_image_btn)
        image_layout.addLayout(image_input_layout)
        
        # Image selection status
        self.image_status_label = QLabel("No image selected")
        self.image_status_label.setStyleSheet("color: #888888;")
        image_layout.addWidget(self.image_status_label)
        
        main_layout.addWidget(image_frame)
        
        # Audio selection - in a frame with border
        audio_frame = QFrame()
        audio_frame.setFrameShape(QFrame.StyledPanel)
        audio_frame.setLineWidth(1)
        audio_layout = QVBoxLayout(audio_frame)
        
        audio_header = QLabel("🔊 AUDIO FILE")
        audio_header.setStyleSheet("font-weight: bold; font-size: 14px;")
        audio_layout.addWidget(audio_header)
        
        audio_desc = QLabel("Select an audio file (speech or singing)")
        audio_layout.addWidget(audio_desc)
        
        audio_input_layout = QHBoxLayout()
        self.audio_path_edit = QLineEdit()
        self.audio_path_edit.setReadOnly(True)
        self.audio_path_edit.setPlaceholderText("No audio selected")
        
        browse_audio_btn = QPushButton("Browse for Audio...")
        browse_audio_btn.setMinimumWidth(150)
        browse_audio_btn.clicked.connect(self.browse_audio)
        
        audio_input_layout.addWidget(self.audio_path_edit)
        audio_input_layout.addWidget(browse_audio_btn)
        audio_layout.addLayout(audio_input_layout)
        
        # Audio selection status
        self.audio_status_label = QLabel("No audio selected")
        self.audio_status_label.setStyleSheet("color: #888888;")
        audio_layout.addWidget(self.audio_status_label)
        
        main_layout.addWidget(audio_frame)
        
        # Options group
        options_group = QGroupBox("Processing Options")
        options_layout = QVBoxLayout(options_group)
        
        # Checkboxes
        self.enhancer_checkbox = QCheckBox("Use Face Enhancer (GFPGAN) - Improves output quality")
        self.enhancer_checkbox.setChecked(True)
        self.cpu_checkbox = QCheckBox("Use CPU (slower but more compatible with all systems)")
        self.full_body_checkbox = QCheckBox("Full Body Mode - Use for images showing more than just the face")
        
        options_layout.addWidget(self.enhancer_checkbox)
        options_layout.addWidget(self.cpu_checkbox)
        options_layout.addWidget(self.full_body_checkbox)
        
        # Preprocess method
        preprocess_layout = QHBoxLayout()
        preprocess_label = QLabel("Preprocess Method:")
        self.preprocess_combo = QComboBox()
        self.preprocess_combo.addItems(["crop", "extcrop", "resize", "full", "extfull"])
        preprocess_desc = QLabel("(Use 'full' for full body images)")
        preprocess_desc.setStyleSheet("color: #666666;")
        
        preprocess_layout.addWidget(preprocess_label)
        preprocess_layout.addWidget(self.preprocess_combo)
        preprocess_layout.addWidget(preprocess_desc)
        preprocess_layout.addStretch()
        options_layout.addLayout(preprocess_layout)
        
        main_layout.addWidget(options_group)
        
        # Generate button
        self.generate_btn = QPushButton("Generate Talking Face Video")
        self.generate_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; font-weight: bold;")
        self.generate_btn.setMinimumHeight(50)
        self.generate_btn.clicked.connect(self.generate_video)
        main_layout.addWidget(self.generate_btn)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        main_layout.addWidget(self.progress_bar)
        
        # Log area
        log_group = QGroupBox("Processing Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_group, 1)  # Give it a stretch factor
        
        # Output video section
        result_frame = QFrame()
        result_frame.setFrameShape(QFrame.StyledPanel)
        result_frame.setLineWidth(1)
        result_layout = QVBoxLayout(result_frame)
        
        result_header = QLabel("🎬 OUTPUT VIDEO")
        result_header.setStyleSheet("font-weight: bold; font-size: 14px;")
        result_layout.addWidget(result_header)
        
        result_input_layout = QHBoxLayout()
        result_label = QLabel("Generated Video:")
        self.result_path_edit = QLineEdit()
        self.result_path_edit.setReadOnly(True)
        self.result_path_edit.setPlaceholderText("No video generated yet")
        open_folder_btn = QPushButton("Open Folder")
        open_folder_btn.clicked.connect(self.open_result_folder)
        
        result_input_layout.addWidget(result_label)
        result_input_layout.addWidget(self.result_path_edit)
        result_input_layout.addWidget(open_folder_btn)
        result_layout.addLayout(result_input_layout)
        
        main_layout.addWidget(result_frame)
        
        # Set main widget
        self.setCentralWidget(main_widget)
    
    def browse_image(self):
        # Create a file dialog with options to ensure video files are selectable
        dialog = QFileDialog(self)
        dialog.setWindowTitle("Select Source Image or Video")
        
        # Set the filter but make it more explicit
        filters = "All Media Files (*.png *.jpg *.jpeg *.bmp *.mp4 *.avi *.mov *.webm);;Images (*.png *.jpg *.jpeg *.bmp);;Videos (*.mp4 *.avi *.mov *.webm);;All Files (*)"
        dialog.setNameFilter(filters)
        dialog.setFileMode(QFileDialog.ExistingFile)
        
        # Set initial filter to show all supported files
        dialog.selectNameFilter("All Media Files (*.png *.jpg *.jpeg *.bmp *.mp4 *.avi *.mov *.webm)")
        
        if dialog.exec_():
            selected_files = dialog.selectedFiles()
            if selected_files:
                file_path = selected_files[0]
                self.source_image_path = file_path
                self.image_path_edit.setText(file_path)
                
                # Update status with file info
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path) / 1024  # KB
                
                if file_name.lower().endswith(('.mp4', '.avi', '.mov', '.webm')):
                    self.image_status_label.setText(f"Selected Video: {file_name} ({file_size/1024:.1f} MB)")
                    self.image_status_label.setStyleSheet("color: #0000FF; font-weight: bold;")
                else:
                    self.image_status_label.setText(f"Selected Image: {file_name} ({file_size:.1f} KB)")
                    self.image_status_label.setStyleSheet("color: #008800; font-weight: bold;")
    
    def browse_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Audio File", "", 
            "Audio Files (*.wav *.mp3);;All Files (*)"
        )
        if file_path:
            self.audio_path = file_path
            self.audio_path_edit.setText(file_path)
            
            # Update status with file info
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / 1024  # KB
            self.audio_status_label.setText(f"Selected: {file_name} ({file_size:.1f} KB)")
            self.audio_status_label.setStyleSheet("color: #008800; font-weight: bold;")
    
    def log(self, message):
        self.log_text.append(message)
        # Scroll to the bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def open_result_folder(self):
        if not self.result_path:
            QMessageBox.warning(self, "Warning", "No output video has been generated yet.")
            return
            
        result_dir = os.path.dirname(self.result_path)
        if os.path.exists(result_dir):
            if sys.platform == 'darwin':  # macOS
                subprocess.call(['open', result_dir])
            elif sys.platform == 'win32':  # Windows
                os.startfile(result_dir)
            else:  # Linux
                subprocess.call(['xdg-open', result_dir])
        else:
            QMessageBox.warning(self, "Error", "Output folder doesn't exist.")
    
    def generate_video(self):
        # Validate inputs
        if not self.source_image_path:
            QMessageBox.warning(self, "Warning", "Please select a source image.")
            return
        
        if not self.audio_path:
            QMessageBox.warning(self, "Warning", "Please select an audio file.")
            return
        
        # Prepare command
        command = ["python", "inference.py", 
                  "--driven_audio", self.audio_path,
                  "--source_image", self.source_image_path]
        
        if self.enhancer_checkbox.isChecked():
            command.extend(["--enhancer", "gfpgan"])
            
        if self.cpu_checkbox.isChecked():
            command.append("--cpu")
            
        if self.full_body_checkbox.isChecked():
            command.append("--still")
            
        command.extend(["--preprocess", self.preprocess_combo.currentText()])
        
        # Start processing
        self.log(f"Starting SadTalker with command: {' '.join(command)}")
        self.progress_bar.setRange(0, 0)  # Indeterminate mode
        self.generate_btn.setEnabled(False)
        
        # Start processing thread
        self.process_thread = ProcessThread(command)
        self.process_thread.output_received.connect(self.log)
        self.process_thread.process_finished.connect(self.process_finished)
        self.process_thread.video_path_found.connect(self.set_result_path)
        self.process_thread.start()
    
    def set_result_path(self, path):
        self.result_path = path
        self.result_path_edit.setText(path)
    
    def process_finished(self, return_code):
        self.progress_bar.setRange(0, 1)  # Back to normal mode
        self.progress_bar.setValue(1 if return_code == 0 else 0)
        self.generate_btn.setEnabled(True)
        
        if return_code == 0:
            self.log("Processing completed successfully!")
            QMessageBox.information(self, "Success", "Video generation completed successfully!")
        else:
            self.log(f"Process failed with return code {return_code}")
            QMessageBox.critical(self, "Error", f"Video generation failed with error code {return_code}")

def main():
    app = QApplication(sys.argv)
    window = SadTalkerUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 