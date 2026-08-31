from langchain_google_community import CalendarToolkit

toolkit=CalendarToolkit()

calendar_tools=[tool for tool in toolkit.get_tools() if "delete" not in tool.name.lower()]

# tool=[tool.name for tool in toolkit.get_tools()]
# print(tool)