"""
Backup Controller Module for Smart Farmer Assistant.

Manages offline database JSON backup export and restoration operations for platform administrators.
"""

from typing import Dict, Any, Tuple, Union
from flask import request, jsonify, render_template, Response, send_file
from app.controllers.base_controller import BaseController
from app.services.system_backup_restore_service import SystemBackupRestoreService
import logging

logger = logging.getLogger(__name__)


class BackupController(BaseController):
    """
    Controller providing database JSON snapshot export and admin database backup management.
    """

    def __init__(self):
        self.backup_service = SystemBackupRestoreService()

    def export_backup(self) -> Union[Response, Tuple[Response, int]]:
        """
        Creates and downloads JSON database snapshot archive.
        """
        if not self.is_admin():
            return self.error_response(message="Admin access required", status_code=403)

        try:
            backup_res = self.backup_service.create_database_backup()
            filepath = backup_res["filepath"]

            if request.is_json:
                return self.success_response(data=backup_res, message="Database backup generated successfully")

            return send_file(
                filepath,
                mimetype="application/json",
                as_attachment=True,
                download_name=backup_res["filename"]
            )

        except Exception as e:
            return self.handle_exception(e, "Error creating database backup")
