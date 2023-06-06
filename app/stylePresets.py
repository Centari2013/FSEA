colors = {
    "FRAME_COLOR": "#31353D",
    "SEARCH_BUTTON_COLOR": "#6B7482",
    "SEARCH_BAR_COLOR": "white",
    "PUSH_BUTTON_TEXT_COLOR": "white",
    "PUSH_BUTTON_COLOR": "#262829",
    "PUSH_BUTTON_PRESSED_COLOR": "#111314",
    "TITLEBAR_BUTTON_COLOR": "#31353D",
    "ERROR_MSG": "#E85D04"
}

stylesheets = {
    "SCROLL_BAR": """QScrollBar:vertical {
            border: 0px solid #999999;
            background: none;
            width:10px;    
            margin: 0px 0px 0px 0px;
        }
        QScrollBar::handle:vertical {         
       
            min-height: 0px;
          	border: 0px solid red;
			border-radius: 4px;
			background-color: grey;
        }
        QScrollBar::add-line:vertical {       
            height: 0px;
            subcontrol-position: bottom;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-line:vertical {
            height: 0 px;
            subcontrol-position: top;
            subcontrol-origin: margin;
        }
        QScrollBar::sub-page:vertical {
        background: none;
        }
        
        QScrollBar::add-page:vertical {
        background: none;
        }"""
}