
def getStyleString():
    return '''
QWidget {
    font-size: 11pt;
    font-family: cambria;
    color: white;
    background-color: black;
    selection-color: black;
    selection-background-color: white;
}
QTableWidget {
    border: none;
}
QHeaderView{
}
QHeaderView::section
{
    font-size: 10pt;
    color: white;
    background-color:black;
    border-style: none;
    border-bottom: 2px solid white;
    border-right: 2px solid white;
}
QTableView{
} 
QTableView::item {
}
QPushButton {
    color: white;
    border: 1px solid white;
}
QPushButton::pressed {
    border: 2px solid white;
}
QGroupBox {
    font-size: 9pt;
    font-weight: bold;
}

QLineEdit {
    color: cyan;
    border: none;
}
QLineEdit:focus {
    border: 1px solid cyan;
}

QRadioButton::indicator::unchecked {
    border: 1px solid white; 
    border-radius: 6px;
}
QRadioButton::indicator::unchecked:hover {
    border: 1.5px solid cyan; 
    border-radius: 6px;
}
QRadioButton::indicator::checked {
    background-color: cyan;
    border-radius: 6px;
}
QProgressBar {
    border: 2px solid white;
    background-color: red;
}
QProgressBar::chunk {
    background-color: green;
}
QTabWidget {
    padding: 5px;
    border: none ;
}
QTabWidget::pane { 
    border: 0; 
}
QTabBar::tab {
    width: 100px;
    font-size: 9pt;
    font-weight: bold;
    background-color: black;
    border: 1px solid white;
    padding: 5px;
    margin-top: 20px;
    margin-left: 10px;
    color: white;
}
QTabBar::tab::selected {
    color: black;
    background-color: white;
}
'''