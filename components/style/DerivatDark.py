
def getStyleString():
    return '''

QWidget
{
    font-size: 8pt;
    font-family: cambria;
    color: white;
    background-color: black;
    selection-color: black;
    selection-background-color: white;
}

QTableWidget {
}
QHeaderView{
}
QHeaderView::section
{
    color: white;
    background-color:black;
    border-style: none;
    border-bottom: 2px solid #fffff8;
    border-right: 2px solid #fffff8;
    
}
QTableView{
} 
QTableView::item {
}

QPushButton {
    font-size: 12pt;
    border: 2px outset white;
}
QPushButton::pressed {
    color: black;
    background-color: white;
    border: 2px inset black;
}

QGroupBox
{
    font-size: 10pt;
    font-weight: bold;
}

QLineEdit {
    color: cyan;
    border: none;
    font-weight: bold;
}

QRadioButton::indicator::unchecked
{
    border: 1px solid white; 
    border-radius: 6px;
}
QRadioButton::indicator::unchecked:hover
{
    border: 1.5px solid cyan; 
    border-radius: 6px;
}
QRadioButton::indicator::checked 
{
    background-color: cyan;
    border-radius: 6px;
}


'''