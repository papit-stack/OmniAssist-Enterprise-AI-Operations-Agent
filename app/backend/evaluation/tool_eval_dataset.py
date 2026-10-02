TOOL_EVAL_CASES = [

    # =====================================================================
    # TOOL: calculator
    # =====================================================================

    # {
    #     "input": "What is 245 * 18?",
    #     "expected_tool": ["calculator"],
    #     "expected_args": [{"expression": "245 * 18"}],
    # },
    # {
    #     "input": "Calculate the square root of 144.",
    #     "expected_tool": ["calculator"],
    #     "expected_args": [{"expression": "144 ** 0.5"}],
    # },

    # # =====================================================================
    # # TOOL: Google Calendar 
    # # =====================================================================

    # {
    #     "input": "Create a calendar event for a client call on Friday at 2 PM.",
    #     "expected_tool": ["create_calendar_event"],
    #     "expected_args": [{"summary": "Client call"}],
    # },

    # {
    #     "input": "What meetings do I have scheduled for this week?",
    #     "expected_tool": ["search_events"],
    #     "expected_args": [{}],
    # },


    # {
    #     "input": "Change the time of my client call on Friday to 3 PM.",
    #     "expected_tool": ["update_calendar_event"],
    #     "expected_args": [{}],
    # },

    # =====================================================================
    # TOOL: search_company_policies
    # =====================================================================

    # --- Company Overview ---
    # {
    #     "input": "When was NovaTech Solutions founded?",
    #     "expected_tool": ["search_company_policies"],
    #     "expected_args": [{"query": "NovaTech founding year"}],
    # },

    # # --- Leave Policy ---
    # {
    #     "input": "What is the annual leave policy?",
    #     "expected_tool": ["search_company_policies"],
    #     "expected_args": [{"query": "annual leave policy"}],
    # },
    # {
    #     "input": "What is the notice period for a regular employee?",
    #     "expected_tool": ["search_company_policies"],
    #     "expected_args": [{"query": "notice period resignation"}],
    # },

    # {
    #     "input": "How do I change my bank account for salary?",
    #     "expected_tool": ["search_company_policies"],
    #     "expected_args": [{"query": "change bank account salary"}],
    # },
    # {
    #     "input": "Who do I contact for IT issues?",
    #     "expected_tool": ["search_company_policies"],
    #     "expected_args": [{"query": "IT helpdesk contact"}],
    # },

    # {
    #     "input": "How do I connect to the office network from home?",
    #     "expected_tool": ["search_company_policies"],
    #     "expected_args": [{"query": "VPN work from home security"}],
    # },
    # {
    #     "input": "How do I appeal if I disagree with my rating?",
    #     "expected_tool": ["search_company_policies"],
    #     "expected_args": [{"query": "rating appeal process"}],
    # },

    # {
    #     "input": "How do I get a mentor?",
    #     "expected_tool": ["search_company_policies"],
    #     "expected_args": [{"query": "mentorship program"}],
    # },

    # # =====================================================================
    # # NO TOOL EXPECTED (general conversation / chitchat)
    # # =====================================================================

    {
        "input": "Hello, how are you?",
        "expected_tool": [None],
        "expected_args": [{}],
    },
    {
        "input": "Tell me a joke.",
        "expected_tool": [None],
        "expected_args": [{}],
    },


    # # =====================================================================
    # # MULTI-TOOL TEST CASES
    # # =====================================================================

    {
        "input": "What's 245 * 18 and what is our leave policy?",
        "expected_tool": ["calculator", ["search_company_policies"]],
        "expected_args": [
            {"expression": "245 * 18"},
            {"query": "leave policy"},
        ],
        "note": "Compound request: calculation + policy lookup. Both tools should be called.",
    },
    {
        "input": "Schedule a meeting with Alice tomorrow at 10 AM and check my calendar for that day.",
        "expected_tool": ["create_calendar_event", "search_events"],
        "expected_args": [
            {"summary": "Meeting with Alice", "start_datetime": "Tomorrow at 10 AM"},
            [{}],
        ],
        "note": "Two intents: create an event and confirm existing scheduled events.",
    },
]