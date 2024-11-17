#
# @savefile.py Copyright (c) 2021 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved. #
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import os
import shutil


class SaveFile():
    def __init__(self):
        super().__init__()
        # Create destiny folder if doesn't exist
        self.download_folder = os.path.join(os.getcwd(), "input_files")
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

    # Function to select and save the file from local machine
    def select_and_save_file(self, file_path):
        # Original file name
        file_name = os.path.basename(file_path)
        # Destiny path in 'downloaded_files' folder
        destination_path = os.path.join(self.download_folder, file_name)
        # Copy the file in destiny folder
        shutil.copy(file_path, destination_path)

        """    except Exception as e:
                #QMessageBox.critical(self, "Error", f"File could not be copied: {e}")
                print("Something failed opening the file")"""
