TOOL_EVAL_CASES = [

    # =====================================================================
    # TOOL: calculator
    # =====================================================================

    # {
    #     "input": "What is 245 * 18?",
    #     "expected_tool": [
    #         {"name": "calculator", "args": {"expression": "245 * 18"}},
    #     ],
    # },
    # {
    #     "input": "Calculate the square root of 144.",
    #     "expected_tool": [
    #         {"name": "calculator", "args": {"expression": "144 ** 0.5"}},
    #     ],
    # },

    # # =====================================================================
    # # TOOL: web_search
    # # =====================================================================

    # {
    #     "input": "What are the latest developments in quantum computing?",
    #     "expected_tool": [
    #         {"name": "web_search", "args": {"query": "latest developments in quantum computing"}},
    #     ],
    # },
    # {
    #     "input": "Search for the current weather in Tokyo.",
    #     "expected_tool": [
    #         {"name": "web_search", "args": {"query": "current weather in Tokyo"}},
    #     ],
    # },
    # {
    #     "input": "Who won the Nobel Prize in Physics this year?",
    #     "expected_tool": [
    #         {"name": "web_search", "args": {"query": "Nobel Prize in Physics 2026 winner"}},
    #     ],
    # },

    # # =====================================================================
    # # TOOL: Google Calendar (create_event)
    # # =====================================================================

    # {
    #     "input": "Schedule a meeting with the design team tomorrow at 10 AM.",
    #     "expected_tool": [
    #         {"name": "create_calendar_event", "args": {"summary": "Meeting with design team", "start_datetime": "Tomorrow at 10 AM"}},
    #     ],
    # },
    {
        "input": "Create a calendar event for a client call on Friday at 2 PM.",
        "expected_tool": [
            {"name": "create_calendar_event", "args": {"summary": "Client call"}},
        ],
    },

    # # =====================================================================
    # # TOOL: Google Calendar (get_events / search_events)
    # # =====================================================================

    {
        "input": "What meetings do I have scheduled for this week?",
        "expected_tool": [
            {"name": "search_events", "args": {}},
        ],
    },
    # {
    #     "input": "Do I have any appointments tomorrow?",
    #     "expected_tool": [
    #         {"name": "search_events", "args": {}},
    #     ],
    # },
    # {
    #     "input": "Show me my calendar for next Monday.",
    #     "expected_tool": [
    #         {"name": "search_events", "args": {}},
    #     ],
    # },

    # # =====================================================================
    # # TOOL: Google Calendar (update_event)
    # # =====================================================================

    # {
    #     "input": "Move my 3 PM meeting today to 4:30 PM.",
    #     "expected_tool": [
    #         {"name": "update_calendar_event", "args": {}},
    #     ],
    # },
    # {
    #     "input": "Change the time of my client call on Friday to 3 PM.",
    #     "expected_tool": [
    #         {"name": "update_calendar_event", "args": {}},
    #     ],
    # },

    # # =====================================================================
    # # TOOL: search_company_policies
    # # =====================================================================

    # # --- Annual Leave ---
    # {
    #     "input": "What is the annual leave policy?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "annual leave policy"}},
    #     ],
    # },
    # {
    #     "input": "How many days before do I need to request vacation?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "annual leave advance notice"}},
    #     ],
    # },
    # {
    #     "input": "Can I take leave during a project deadline?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "leave during project deadline"}},
    #     ],
    # },
    # {
    #     "input": "Does my manager have to approve my leave request?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "leave approval manager"}},
    #     ],
    # },

    # # --- Sick Leave ---
    {
        "input": "What is the sick leave policy?",
        "expected_tool": [
            {"name": "search_company_policies", "args": {"query": "sick leave policy"}},
        ],
    },
    {
        "input": "Do I need a doctor's note for sick leave?",
        "expected_tool": [
            {"name": "search_company_policies", "args": {"query": "sick leave medical documentation"}},
        ],
    },

    # --- Emergency Leave ---
    {
        "input": "How do I request emergency leave?",
        "expected_tool": [
            {"name": "search_company_policies", "args": {"query": "emergency leave request"}},
        ],
    },

    # --- Remote Work ---
    {
        "input": "What is the remote work policy?",
        "expected_tool": [
            {"name": "search_company_policies", "args": {"query": "remote work policy"}},
        ],
    },
    # {
    #     "input": "Do I need approval to work from home?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "remote work manager approval"}},
    #     ],
    # },
    # {
    #     "input": "Can I work remotely from another country?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "remote work from another country"}},
    #     ],
    # },

    # # --- Expense Policy ---
    # {
    #     "input": "What is the expense reimbursement policy?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "expense reimbursement policy"}},
    #     ],
    # },
    # {
    #     "input": "How do I submit an expense claim?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "submit expense claim"}},
    #     ],
    # },
    # {
    #     "input": "What receipts do I need for an expense claim?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "receipts for expense claim"}},
    #     ],
    # },
    # {
    #     "input": "Within how many days should I submit an expense?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "expense submission deadline"}},
    #     ],
    # },
    # {
    #     "input": "Can I claim personal meals as a business expense?",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "personal meals expense claim"}},
    #     ],
    # },

    # # =====================================================================
    # # NO TOOL EXPECTED (general conversation / chitchat)
    # # =====================================================================

    # {
    #     "input": "Hello, how are you?",
    #     "expected_tool": None,
    # },
    # {
    #     "input": "Tell me a joke.",
    #     "expected_tool": None,
    # },
    # {
    #     "input": "What is machine learning?",
    #     "expected_tool": None,
    # },
    # {
    #     "input": "Thank you for your help!",
    #     "expected_tool": None,
    # },

    # # =====================================================================
    # # EDGE CASES / AMBIGUOUS QUERIES
    # # =====================================================================

    # {
    #     "input": "When is my next meeting and how many days of leave do I have left?",
    #     "expected_tool": [
    #         {"name": "search_events", "args": {}},
    #     ],
    #     "note": "Ambiguous - could need search_events and/or search_company_policies. Calendar is primary intent.",
    # },
    # {
    #     "input": "I want to schedule time off next week.",
    #     "expected_tool": [
    #         {"name": "search_company_policies", "args": {"query": "scheduling time off leave"}},
    #     ],
    #     "note": "User wants to take leave; should consult leave policy first before creating a calendar event.",
    # },

    # =====================================================================
    # MULTI-TOOL TEST CASES
    # =====================================================================

    # {
    #     "input": "What's 2 + 2 and what's our leave policy?",
    #     "expected_tool": [
    #         {"name": "calculator", "args": {"expression": "2 + 2"}},
    #         {"name": "search_company_policies", "args": {"query": "leave policy"}},
    #     ],
    #     "note": "Compound request: calculation + policy lookup. Both tools should be called.",
    # },
    # {
    #     "input": "Schedule a meeting with Alice tomorrow at 10 AM, and search for her latest project documents.",
    #     "expected_tool": [
    #         {"name": "create_calendar_event", "args": {"summary": "Meeting with Alice", "start_datetime": "Tomorrow at 10 AM"}},
    #         {"name": "web_search", "args": {"query": "Alice latest project documents"}},
    #     ],
    #     "note": "Two distinct intents: calendar event creation + web search.",
    # },
    # {
    #     "input": "Find me a restaurant nearby and schedule a lunch meeting.",
    #     "expected_tool": [
    #         {"name": "web_search", "args": {"query": "restaurant nearby"}},
    #         {"name": "create_calendar_event", "args": {"summary": "Lunch meeting"}},
    #     ],
    #     "note": "Two intents; web search first, then calendar. Both tools should be called.",
    # },
]
