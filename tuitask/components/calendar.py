import calendar
from datetime import date
from rich.text import Text
from textual.containers import Container
from textual.widgets import Label
from textual.widget import Widget
from textual.app import ComposeResult

class CalendarWidget(Widget):
    """Custom Calendar Widget rendering via Rich Text."""
    
    def render(self) -> Text:
        today = date.today()
        # Fixed reference date 17-23 Nov for demo as requested
        
        cal = calendar.Calendar(firstweekday=calendar.SUNDAY)
        # Using Nov 2024 as per screenshot context (17 Nov is Sunday)
        year = 2024 
        month = 11
        
        output = Text()
        
        # 1. Header
        header_str = "  S   M   T   W   T   F   S"
        output.append(header_str + "\n", style="bold text-muted")
        
        # 2. Days
        month_days = cal.monthdayscalendar(year, month)
        
        range_start = 17
        range_end = 23
        
        for week in month_days:
            line = Text()
            for i, day in enumerate(week):
                if day == 0:
                    day_str = "    "
                else:
                    day_str = f"{day:>2} "
                    if day < 10:
                         day_str = f" {day}  "
                    else:
                         day_str = f"{day}  "
                
                if day == 0:
                    cell_text = Text("    ")
                else:
                    cell_text = Text(f"{day:>3} ")
                
                if range_start <= day <= range_end and day != 0:
                     cell_text.stylize("reverse")
                elif day == 0:
                     cell_text.stylize("dim")
                else:
                     pass
                     
                line.append(cell_text)
            
            output.append(line)
            output.append("\n")
            
        return output

class CalendarPanel(Container):
    def compose(self) -> ComposeResult:
        self.border_title = "View and add"
        self.add_class("card")
        
        with Container(id="mode_tabs"):
            yield Label("Expense   Income", classes="mode-labels")
            
        with Container(id="period_row"):
            yield Label("Period   <<< 17 Nov - 23 Nov >>>", classes="period-text")
            
        yield CalendarWidget(id="calendar_grid")
