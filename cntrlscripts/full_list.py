import datetime
import os
import subprocess
import sys
import shlex

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QWidget,
    QStyle,
    QCheckBox
)

# PyQt6 port of cntrlscripts/full_list.py -- same behavior (list every
# config under configs/, color-code it by folder, filter/sort it, launch it
# via player.py/multiplayer.py/sequencer.v2.py, kill running pieces), just
# windowed with PyQt6 instead of tkinter/tkmacosx.

configPath = "/Users/lamshell/Documents/Dev/LEDELI/RPI/configs/"
base = "/Users/lamshell/Documents/Dev/LEDELI/RPI/"

_defaultClr = "#029eed"
_stopAndRun = "#0277ed"
_quitClr = "#74144c"
_stopAllClr = "#9e1b67"

_prodColor = "#85f3d6"
_stagingColor = "#fafad3"
_devFormsClr = "#79fcf3"
_devClr = "#cef7f8"
_devOnDeckClr = "#ccFF00"
_screenGridClr = "#eeeeee"
_reference = "#adc4fd"

usePygamePlayer = False

class bcolors:
    WARNING = "\033[93m"
    ENDC = "\033[0m"


def log_message(text):
    print(f">> {text}")


def _rowColor(key):
    # Mirrors full_list.py's chained itemconfig calls: later category
    # matches override earlier ones, unmatched rows stay white.
    color = _prodColor if "prod" in key else "#ffffff"
    if "staging" in key:
        color = _stagingColor
    if "dev/" in key:
        color = _devClr
    if "forms" in key:
        color = _devFormsClr
    if "studio" in key:
        color = _devOnDeckClr
    if "screen_grid" in key:
        color = _screenGridClr
    if "reference-configs" in key:
        color = _reference
    return color


def _get_config_files(configPath, filterText):
    fullList = []
    filterResults = len(filterText) > 1
    for root, dirs, files in os.walk(configPath, topdown=False):
        for name in files:
            fullPath = os.path.join(root, name)
            if name.endswith(".cfg") and not name.endswith(".py") and name != ".DS_Store":
                res = os.stat(fullPath)
                if "asset_configs" not in fullPath and "/marks" not in fullPath and "/textures" not in fullPath and "/colors" not in fullPath and "/disturbances" not in fullPath and "/palettes" not in fullPath and "/combsets" not in fullPath:
                    if not filterResults and "non_working" not in fullPath:
                        fullList.append((fullPath, res.st_mtime, name))
                    elif name.find(filterText) > 0 or fullPath.find(filterText) > 0:
                        if filterText == "non_working" and "non_working" in fullPath or "non_working" not in fullPath:
                            fullList.append((fullPath, res.st_mtime, name))
    return fullList


def _create_action_dict(fullList, dateSort, configPath):
    actionDict = [{"": ""}]
    lastDir = ""
    for f in fullList:
        if f:
            tsSearchField = datetime.datetime.fromtimestamp(f[1]).strftime("%Y-%m-%d [%H:%M]")
            currentDir = os.path.dirname(f[0].split(configPath)[1]).lstrip("/")
            if currentDir != lastDir and not dateSort:
                actionDict.append({"": ""})
                lastDir = currentDir
            if dateSort:
                actionDict.append({f"{tsSearchField}\t{f[2]}\t\t [{currentDir}]": f[0]})
            else:
                actionDict.append({f"[{currentDir}] \t {tsSearchField} \t\t {f[2]}": f[0]})
        else:
            actionDict.append({"": ""})
    return actionDict


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.running_procs = {}
        self.actionDict1 = []
        self.javaAppRunning = ""
        self._buildUi()
        self.getAllConfigFiles(dateSort=True, subsortDate=True)

    # -------------------------------- #
    # UI construction
    def checkbox_state_changed(self, state):
        global usePygamePlayer
        if state == 2:  # Checked state
            usePygamePlayer = True
        else:
            usePygamePlayer = False

    def _buildUi(self):
        self.setWindowTitle("full_list (PyQt)")
        
        # self.setStyleSheet("background-color: white;")
        self.setFont(QFont(self.font().family(), 12))

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(round(screen.width() - 870), 40, 860, 740)

        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(2, 34, 700, 700)
        self.listWidget.setStyleSheet("background-color: white; color: black;")

        self.searchField = QLineEdit(self)
        self.searchField.setGeometry(2, 2, 270, 26)
        # self.searchField.

        self.windowingCheckbox = QCheckBox('Use PyGame', self)
        self.windowingCheckbox.setChecked(False)  # Set checkbox to checked
        self.windowingCheckbox.stateChanged.connect(self.checkbox_state_changed)
        self.windowingCheckbox.setGeometry(440,2,100,26)


        leftBtnPlace = 725
        topBtnPlace = 8
        btnW, btnH, gap = 120, 24, 28

        def addButton(row, text, bg, fg, command):
            btn = QPushButton(text, self)
            btn.setGeometry(leftBtnPlace, topBtnPlace + row * gap, btnW, btnH)
            btn.setStyleSheet(f"background-color: {bg}; color: {fg}; border: none;")
            btn.clicked.connect(command)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            return btn

        addButton(0, "Stop & Run", _stopAndRun, "white", self.action2)
        addButton(1, "Run", _stopAndRun, "white", self.action)
        addButton(2, "Open", _defaultClr, "white", self.openFile)
        addButton(3, "Sort By Date", _defaultClr, "white", self.sortByDate)
        addButton(4, "Sort by Folder", _defaultClr, "white", self.sortByFolder)
        addButton(5, "Sort by Folder+", _defaultClr, "white", self.sortByFolderAndDate)
        addButton(6, "base-controlled", _devOnDeckClr, "black", lambda: self.ondeck("base-controlled", False, True))
        addButton(7, "Staging", _stagingColor, "black", lambda: self.ondeck("staging", False))
        addButton(8, "Production", _prodColor, "black", lambda: self.ondeck("prod", False))
        addButton(9, "Dev", _devClr, "black", lambda: self.ondeck("dev"))
        addButton(10, "Reference", _reference, "black", lambda: self.ondeck("reference", False))
        addButton(11, "Stop All", _stopAllClr, "white", self.stopAll)
        addButton(12, "QUIT", _quitClr, "white", self.quitApp)

        clearButton = QPushButton("Clear", self)
        clearButton.setGeometry(280, 2, btnW, 26)
        clearButton.setStyleSheet(f"background-color: {_defaultClr}; color: white; border: none;")
        clearButton.clicked.connect(self.clear)
        clearButton.setCursor(Qt.CursorShape.PointingHandCursor)

    # -------------------------------- #
    # Selection / process control

    def verify(self):
        row = self.listWidget.currentRow()
        if row is not None and row >= 0:
            return True, self.actionDict1[row]
        return False, None

    def execute(self, configToRun):
        log_message(f"{bcolors.WARNING}")
        log_message("\n\n---------------------------------------------------------------------------------------")
        log_message("full_list_pyqt.py app window is calling this to run: ")
        log_message(configToRun.split(configPath)[1])

        cfg_rel = configToRun.split(configPath)[1]

        if ".cfg" in configToRun:
            if "multi" in configToRun:
                log_message("MULTIPLAYER STARTING >>>\n")
                cmd = ["python3", "-u", base + "multiplayer.py", "-path", base, "-mname", "studio", "-cfg", cfg_rel]
            elif "--manifest" in configToRun:
                cmd = ["python3", "-u", base + "sequencer.v2.py", "-path", base, "-mname", "studio", "-cfg", cfg_rel]
                log_message(" ".join(cmd))
            else:
                if usePygamePlayer:
                    cmd = ["python3", "-u", base + "player_pygame.py", "-path", base, "-mname", "studio", "-cfg", cfg_rel]
                else :
                    cmd = ["python3", "-u", base + "player.py", "-path", base, "-mname", "studio", "-cfg", cfg_rel]

            proc = subprocess.Popen(cmd, text=True, bufsize=1)
            self.running_procs[configToRun] = proc
            log_message(f"[started] {cfg_rel}")

        elif ".app" in configToRun:
            os.system(f"open {configToRun.split(configPath)[1]}")
            self.javaAppRunning = configToRun.split(configPath)[1]

        print(f"---------------------------------------------------------------------------------------\n\n\n{bcolors.ENDC}")

    def action(self):
        ok, configSelected = self.verify()
        if ok:
            configToRun = configSelected[list(configSelected.keys())[0]]
            self.execute(configToRun)

    def action2(self):
        ok, configSelected = self.verify()
        if ok:
            os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")
            os.system("ps -ef | pgrep -f Player | xargs sudo kill -9;")
            # cmd = "ps -ef | pgrep -f player | xargs sudo kill -9;"
            # args = shlex.split(cmd)

            # print(args)
            # exit()
            # # subprocess.run(args)
            # subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # # os.system("ps -ef | pgrep -f Player | xargs sudo kill -9;")

            if self.javaAppRunning != "":
                os.system(f"ps -ef | pgrep -f {self.javaAppRunning} | xargs sudo kill -9;")

            configToRun = configSelected[list(configSelected.keys())[0]]
            self.execute(configToRun)

    def openFile(self):
        ok, configSelected = self.verify()
        if ok:
            # os.system(f"open {configSelected[list(configSelected.keys())[0]]}")
            cmd = f"open {configSelected[list(configSelected.keys())[0]]}"
            args = shlex.split(cmd)
            subprocess.run(args)

    def stopAll(self):
        os.system("ps -ef | pgrep -f player | xargs sudo kill -9;")
        os.system("ps -ef | pgrep -f sequencer | xargs sudo kill -9;")
        # cmd = "ps -ef | pgrep -fi player | xargs sudo kill -9;"
        # args = shlex.split(cmd)
        # subprocess.run(args)

    def quitApp(self):
        QApplication.instance().quit()

    # -------------------------------- #
    # Search / sort / list population

    def clear(self):
        self.searchField.clear()

    def sortByDate(self):
        self.getAllConfigFiles(dateSort=True, subsortDate=False, filterText=self.searchField.text())

    def sortByFolder(self):
        self.getAllConfigFiles(dateSort=False, subsortDate=False, filterText=self.searchField.text())

    def sortByFolderAndDate(self):
        self.getAllConfigFiles(dateSort=False, subsortDate=True)

    def ondeck(self, arg, dateSort=True, subsortDate=True):
        self.searchField.setText(arg)
        self.getAllConfigFiles(dateSort=dateSort, subsortDate=subsortDate, filterText=arg)

    def getAllConfigFiles(self, dateSort=False, subsortDate=False, filterText=""):
        fullList = _get_config_files(configPath, filterText)

        if dateSort:
            fullList.sort(key=lambda f: f[1], reverse=True)
        else:
            fullList.sort(key=lambda f: f[0], reverse=False)

        self.actionDict1 = _create_action_dict(fullList, dateSort, configPath)

        self.listWidget.clear()
        for item in self.actionDict1:
            self._addListItem(item)

    def _addListItem(self, item):
        key = list(item.keys())[0]
        listItem = QListWidgetItem(f" {key}")
        listItem.setBackground(QColor(_rowColor(key)))
        listItem.setForeground(QColor("black"))
        self.listWidget.addItem(listItem)


def main():
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('chip_icon_normal.png'))
    path = os.path.join(os.path.dirname(sys.modules[__name__].__file__), 'leddeliico/ledeliapp.png')
    
    app.setWindowIcon(QIcon(path))
    panel = ControlPanel()
    panel.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
