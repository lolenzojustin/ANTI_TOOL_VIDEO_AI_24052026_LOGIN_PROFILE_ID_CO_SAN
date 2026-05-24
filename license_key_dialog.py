# -*- coding: utf-8 -*-
"""
Module giao diện nhập License Key.
Người dùng bắt buộc phải nhập đúng license key còn hạn mới vào được giao diện tool.
Import vào file chạy chính:
    from license_key_dialog import LicenseKeyDialog
Sử dụng:
    dialog = LicenseKeyDialog()
    if not dialog.exec_accepted():
        sys.exit(0)
"""

from PyQt5 import QtCore, QtGui, QtWidgets

# ══════════════════════════════════════════════════════════════
# License key hợp lệ (có thể mở rộng thành danh sách hoặc gọi API sau này)
# ══════════════════════════════════════════════════════════════
VALID_LICENSE_KEYS = [
    "Thang@123",
]


class LicenseKeyDialog(QtWidgets.QDialog):
    """Dialog yêu cầu người dùng nhập License Key trước khi vào tool."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xác thực License Key")
        self.setFixedSize(520, 420)
        self.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.WindowCloseButtonHint
            | QtCore.Qt.MSWindowsFixedSizeDialogHint
        )
        self._accepted = False
        self._build_ui()
        self._apply_styles()

    # ──────────────────────────────────────────────
    # Xây dựng giao diện
    # ──────────────────────────────────────────────
    def _build_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── Container chính ──
        container = QtWidgets.QFrame()
        container.setObjectName("licenseContainer")
        container_layout = QtWidgets.QVBoxLayout(container)
        container_layout.setContentsMargins(40, 30, 40, 30)
        container_layout.setSpacing(0)

        # ── Icon khoá ──
        icon_label = QtWidgets.QLabel("🔐")
        icon_label.setObjectName("licenseIcon")
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        container_layout.addWidget(icon_label)

        container_layout.addSpacing(10)

        # ── Tiêu đề ──
        title = QtWidgets.QLabel("XÁC THỰC BẢN QUYỀN")
        title.setObjectName("licenseTitle")
        title.setAlignment(QtCore.Qt.AlignCenter)
        container_layout.addWidget(title)

        container_layout.addSpacing(6)

        # ── Mô tả ──
        subtitle = QtWidgets.QLabel(
            "Vui lòng nhập License Key để kích hoạt và sử dụng tool.\n"
            "Liên hệ Admin nếu bạn chưa có key bản quyền."
        )
        subtitle.setObjectName("licenseSubtitle")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        subtitle.setWordWrap(True)
        container_layout.addWidget(subtitle)

        container_layout.addSpacing(24)

        # ── Label ô nhập ──
        input_label = QtWidgets.QLabel("LICENSE KEY")
        input_label.setObjectName("inputLabel")
        container_layout.addWidget(input_label)

        container_layout.addSpacing(6)

        # ── Ô nhập license key ──
        self.le_license = QtWidgets.QLineEdit()
        self.le_license.setObjectName("licenseInput")
        self.le_license.setPlaceholderText("Nhập license key tại đây...")
        self.le_license.setFixedHeight(46)
        self.le_license.setEchoMode(QtWidgets.QLineEdit.Password)
        container_layout.addWidget(self.le_license)

        container_layout.addSpacing(8)

        # ── Checkbox hiện/ẩn key ──
        self.cb_show = QtWidgets.QCheckBox("Hiển thị License Key")
        self.cb_show.setObjectName("showKeyCheckbox")
        self.cb_show.setCursor(QtCore.Qt.PointingHandCursor)
        self.cb_show.toggled.connect(self._toggle_echo)
        container_layout.addWidget(self.cb_show)

        container_layout.addSpacing(16)

        # ── Thông báo lỗi (ẩn mặc định) ──
        self.lb_error = QtWidgets.QLabel("")
        self.lb_error.setObjectName("licenseError")
        self.lb_error.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_error.setWordWrap(True)
        self.lb_error.setVisible(False)
        container_layout.addWidget(self.lb_error)

        container_layout.addSpacing(10)

        # ── Nút kích hoạt ──
        self.btn_activate = QtWidgets.QPushButton("🔓  KÍCH HOẠT BẢN QUYỀN")
        self.btn_activate.setObjectName("activateBtn")
        self.btn_activate.setFixedHeight(48)
        self.btn_activate.setCursor(QtCore.Qt.PointingHandCursor)
        self.btn_activate.clicked.connect(self._on_activate)
        container_layout.addWidget(self.btn_activate)

        container_layout.addStretch()

        # ── Footer ──
        footer = QtWidgets.QLabel("© 2026 Video AI Tool — All rights reserved")
        footer.setObjectName("licenseFooter")
        footer.setAlignment(QtCore.Qt.AlignCenter)
        container_layout.addWidget(footer)

        main_layout.addWidget(container)

        # Enter để kích hoạt
        self.le_license.returnPressed.connect(self._on_activate)

    # ──────────────────────────────────────────────
    # Xử lý sự kiện
    # ──────────────────────────────────────────────
    def _toggle_echo(self, checked):
        if checked:
            self.le_license.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.le_license.setEchoMode(QtWidgets.QLineEdit.Password)

    def _on_activate(self):
        key = self.le_license.text().strip()
        if not key:
            self._show_error("⚠️  Vui lòng nhập License Key!")
            return
        if key in VALID_LICENSE_KEYS:
            self._accepted = True
            self.accept()
        else:
            self._show_error("❌  License Key không hợp lệ hoặc đã hết hạn!\nVui lòng kiểm tra lại hoặc liên hệ Admin.")
            self.le_license.selectAll()
            self.le_license.setFocus()

    def _show_error(self, msg):
        self.lb_error.setText(msg)
        self.lb_error.setVisible(True)
        # Hiệu ứng rung nhẹ
        self._shake_animation()

    def _shake_animation(self):
        """Hiệu ứng rung nhẹ khi nhập sai."""
        anim = QtCore.QPropertyAnimation(self, b"pos")
        anim.setDuration(300)
        pos = self.pos()
        anim.setKeyValueAt(0, pos)
        anim.setKeyValueAt(0.1, pos + QtCore.QPoint(8, 0))
        anim.setKeyValueAt(0.2, pos + QtCore.QPoint(-8, 0))
        anim.setKeyValueAt(0.3, pos + QtCore.QPoint(6, 0))
        anim.setKeyValueAt(0.4, pos + QtCore.QPoint(-6, 0))
        anim.setKeyValueAt(0.5, pos + QtCore.QPoint(4, 0))
        anim.setKeyValueAt(0.6, pos + QtCore.QPoint(-4, 0))
        anim.setKeyValueAt(0.7, pos + QtCore.QPoint(2, 0))
        anim.setKeyValueAt(0.8, pos + QtCore.QPoint(-2, 0))
        anim.setKeyValueAt(1.0, pos)
        anim.start()
        # Giữ tham chiếu để animation không bị GC xoá
        self._anim = anim

    def exec_accepted(self):
        """Chạy dialog và trả về True nếu key hợp lệ, False nếu đóng/thoát."""
        result = self.exec_()
        return self._accepted and result == QtWidgets.QDialog.Accepted

    def closeEvent(self, event):
        """Khi người dùng bấm X đóng dialog thì không cho vào tool."""
        if not self._accepted:
            event.accept()
        else:
            event.accept()

    # ──────────────────────────────────────────────
    # Giao diện CSS (phong cách đồng bộ với tool chính)
    # ──────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            /* ── Container chính ── */
            #licenseContainer {
                background: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #07111f, stop:0.5 #0a1628, stop:1 #07111f
                );
                border: 1px solid #1e3a5f;
                border-radius: 12px;
            }

            /* ── Icon ── */
            #licenseIcon {
                font-size: 52px;
                background: transparent;
                border: none;
            }

            /* ── Tiêu đề ── */
            #licenseTitle {
                color: #ffffff;
                font-size: 22px;
                font-weight: bold;
                letter-spacing: 3px;
                background: transparent;
                border: none;
            }

            /* ── Phụ đề ── */
            #licenseSubtitle {
                color: #94a3b8;
                font-size: 12px;
                line-height: 1.5;
                background: transparent;
                border: none;
            }

            /* ── Label ô nhập ── */
            #inputLabel {
                color: #7c3aed;
                font-size: 11px;
                font-weight: bold;
                letter-spacing: 2px;
                background: transparent;
                border: none;
            }

            /* ── Ô nhập license key ── */
            #licenseInput {
                background-color: #111827;
                color: #e5e7eb;
                border: 2px solid #1e3a5f;
                border-radius: 8px;
                padding: 0 16px;
                font-size: 15px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            #licenseInput:focus {
                border: 2px solid #7c3aed;
                background-color: #0f172a;
            }
            #licenseInput::placeholder {
                color: #4b5563;
                font-weight: normal;
                letter-spacing: 0px;
            }

            /* ── Checkbox hiện key ── */
            #showKeyCheckbox {
                color: #64748b;
                font-size: 11px;
                background: transparent;
                border: none;
                spacing: 6px;
            }
            #showKeyCheckbox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #475569;
                border-radius: 3px;
                background: #111827;
            }
            #showKeyCheckbox::indicator:checked {
                background: #7c3aed;
                border: 1px solid #7c3aed;
            }

            /* ── Thông báo lỗi ── */
            #licenseError {
                color: #ef4444;
                font-size: 12px;
                font-weight: bold;
                background: #1c0a0a;
                border: 1px solid #7f1d1d;
                border-radius: 6px;
                padding: 8px 12px;
            }

            /* ── Nút kích hoạt ── */
            #activateBtn {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7c3aed, stop:1 #a855f7
                );
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                letter-spacing: 1px;
                border: none;
                border-radius: 8px;
            }
            #activateBtn:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6d28d9, stop:1 #9333ea
                );
            }
            #activateBtn:pressed {
                background: #5b21b6;
            }

            /* ── Footer ── */
            #licenseFooter {
                color: #334155;
                font-size: 10px;
                background: transparent;
                border: none;
            }
        """)
