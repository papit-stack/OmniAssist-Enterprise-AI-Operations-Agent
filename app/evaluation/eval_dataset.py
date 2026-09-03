test_cases = [

    # =========================
    # Annual Leave
    # =========================

    # {
    #     "input": "What is the annual leave policy?",
    #     "expected_output": (
    #         "Annual leave provides paid time off for personal or vacation purposes."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Annual Leave: Paid time off for personal or vacation purposes.\n\n"
    #             "Annual Leave\n\n"
    #             "Employees should submit annual leave requests at least 3 working days "
    #             "before the intended start date.\n\n"
    #             "Annual leave is subject to manager approval and business requirements.\n\n"
    #             "Employees should avoid scheduling leave during critical project deadlines "
    #             "unless prior approval has been obtained."
    #         )
    #     ],
    # },

    {
        "input": "How many days in advance should I request annual leave?",
        "expected_output": (
            "Annual leave requests must be submitted at least 3 working days "
            "before the intended start date."
        ),
        "expected_retrieval_context": [
            (
                "Annual Leave\n\n"
                "Employees should submit annual leave requests at least 3 working days "
                "before the intended start date.\n\n"
                "Annual leave is subject to manager approval and business requirements.\n\n"
                "Employees should avoid scheduling leave during critical project deadlines "
                "unless prior approval has been obtained."
            )
        ],
    },

    {
        "input": "Who approves annual leave requests?",
        "expected_output": (
            "Annual leave approval depends on business requirements, team workload, "
            "project deadlines, existing approved leaves, and available leave balance."
        ),
        "expected_retrieval_context": [
            (
                "Annual leave is subject to manager approval and business requirements.\n\n"
                "Leave Approval\n\n"
                "Submitting a leave request does not guarantee approval.\n\n"
                "Managers consider:\n\n"
                "Team workload\n"
                "Project deadlines\n"
                "Existing approved leave\n"
                "Business continuity\n"
                "The employee's available leave balance\n\n"
                "Employees should wait for approval before making commitments "
                "that depend on the leave being granted."
            )
        ],
    },

    # {
    #     "input": "Can I take annual leave during a critical project deadline?",
    #     "expected_output": (
    #         "Employees should avoid scheduling annual leave during critical project "
    #         "deadlines unless they have prior approval."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Employees should avoid scheduling leave during critical project deadlines "
    #             "unless prior approval has been obtained."
    #         )
    #     ],
    # },

    # {
    #     "input": "Does submitting an annual leave request guarantee approval?",
    #     "expected_output": (
    #         "No. Submitting an annual leave request does not guarantee approval."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Leave Approval\n\n"
    #             "Submitting a leave request does not guarantee approval.\n\n"
    #             "Managers consider:\n\n"
    #             "Team workload\n"
    #             "Project deadlines\n"
    #             "Existing approved leave\n"
    #             "Business continuity\n"
    #             "The employee's available leave balance"
    #         )
    #     ],
    # },

    # =========================
    # Sick Leave
    # =========================

    # {
    #     "input": "What is the sick leave policy?",
    #     "expected_output": (
    #         "Employees may take sick leave when they are unable to work due to illness "
    #         "according to the company's sick leave policy."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Sick Leave: Leave taken when an employee is ill or requires medical attention.\n\n"
    #             "Sick Leave\n\n"
    #             "Employees should notify their manager as soon as reasonably possible "
    #             "when they are unable to work due to illness.\n\n"
    #             "For extended periods of illness, the company may request appropriate "
    #             "medical documentation in accordance with applicable law and company procedures."
    #         )
    #     ],
    # },

    # {
    #     "input": "How do I request sick leave?",
    #     "expected_output": (
    #         "Employees should notify their manager and follow the company's leave "
    #         "request procedure when taking sick leave."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Sick Leave\n\n"
    #             "Employees should notify their manager as soon as reasonably possible "
    #             "when they are unable to work due to illness.\n\n"
    #             "For extended periods of illness, the company may request appropriate "
    #             "medical documentation in accordance with applicable law and company procedures."
    #         )
    #     ],
    # },

    # {
    #     "input": "Do I need approval for sick leave?",
    #     "expected_output": (
    #         "Employees should follow the company's notification and approval process "
    #         "for sick leave."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Sick Leave\n\n"
    #             "Employees should notify their manager as soon as reasonably possible "
    #             "when they are unable to work due to illness.\n\n"
    #             "For extended periods of illness, the company may request appropriate "
    #             "medical documentation in accordance with applicable law and company procedures."
    #         )
    #     ],
    # },

    # =========================
    # Remote Work
    # =========================

    # {
    #     "input": "What is the remote work policy?",
    #     "expected_output": (
    #         "Remote work is permitted subject to company requirements, business needs, "
    #         "and manager approval."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "REMOTE WORK POLICY\n\n"
    #             "Purpose\n\n"
    #             "This policy establishes guidelines for employees who work remotely "
    #             "or use a hybrid work arrangement.\n\n"
    #             "Eligibility\n\n"
    #             "Remote work eligibility depends on:\n\n"
    #             "Job responsibilities\n"
    #             "Team requirements\n"
    #             "Business needs\n"
    #             "Manager approval\n"
    #             "Employee performance and reliability\n\n"
    #             "Not all roles are suitable for remote work."
    #         )
    #     ],
    # },

    # {
    #     "input": "Who can work remotely?",
    #     "expected_output": (
    #         "Employees may work remotely when their role and business requirements "
    #         "allow it and the appropriate approval has been obtained."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Eligibility\n\n"
    #             "Remote work eligibility depends on:\n\n"
    #             "Job responsibilities\n"
    #             "Team requirements\n"
    #             "Business needs\n"
    #             "Manager approval\n"
    #             "Employee performance and reliability\n\n"
    #             "Not all roles are suitable for remote work."
    #         )
    #     ],
    # },

    # {
    #     "input": "Does remote work require manager approval?",
    #     "expected_output": (
    #         "Yes, remote work may require manager approval depending on company policy "
    #         "and business requirements."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Eligibility\n\n"
    #             "Remote work eligibility depends on:\n\n"
    #             "Job responsibilities\n"
    #             "Team requirements\n"
    #             "Business needs\n"
    #             "Manager approval\n"
    #             "Employee performance and reliability\n\n"
    #             "Not all roles are suitable for remote work."
    #         )
    #     ],
    # },

    # =========================
    # Expense Policy
    # =========================

    # {
    #     "input": "What expenses can employees claim?",
    #     "expected_output": (
    #         "Employees can claim approved business expenses incurred during official "
    #         "company activities."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Eligible Expenses\n\n"
    #             "Reasonable and necessary expenses incurred for legitimate business "
    #             "purposes may be reimbursable.\n\n"
    #             "Examples include:\n\n"
    #             "Business travel\n"
    #             "Transportation\n"
    #             "Accommodation\n"
    #             "Business meals\n"
    #             "Client or business meetings\n"
    #             "Approved conferences and events\n"
    #             "Other expenses specifically authorized by the company"
    #         )
    #     ],
    # },

    # {
    #     "input": "How do I submit an expense claim?",
    #     "expected_output": (
    #         "Employees should submit expenses through the company's expense "
    #         "reimbursement process with the required documentation."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Expense Submission\n\n"
    #             "Employees should submit expense claims within 30 days of the expense "
    #             "unless their department has a different deadline.\n\n"
    #             "Each expense claim should include:\n\n"
    #             "Expense date\n"
    #             "Amount\n"
    #             "Currency\n"
    #             "Business purpose\n"
    #             "Appropriate category\n"
    #             "Supporting receipt or documentation"
    #         )
    #     ],
    # },

    # {
    #     "input": "What documents are required for expense reimbursement?",
    #     "expected_output": (
    #         "Employees should provide the required supporting documentation, such as "
    #         "receipts, when submitting an expense claim."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Receipts\n\n"
    #             "Employees must retain receipts or other required supporting "
    #             "documentation for reimbursable expenses.\n\n"
    #             "Receipts should clearly show:\n\n"
    #             "Date\n"
    #             "Vendor\n"
    #             "Amount\n"
    #             "Description of the expense\n\n"
    #             "If a receipt is unavailable, the employee should follow the company's "
    #             "approved missing-receipt procedure."
    #         )
    #     ],
    # },

    # =========================
    # Conversational Queries
    # =========================

    # {
    #     "input": "I want to take annual leave. How many days before should I ask?",
    #     "expected_output": (
    #         "Annual leave requests must be submitted at least 3 working days "
    #         "before the intended start date."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Annual Leave\n\n"
    #             "Employees should submit annual leave requests at least 3 working days "
    #             "before the intended start date.\n\n"
    #             "Annual leave is subject to manager approval and business requirements.\n\n"
    #             "Employees should avoid scheduling leave during critical project deadlines "
    #             "unless prior approval has been obtained."
    #         )
    #     ],
    # },

    # {
    #     "input": "What about remote work?",
    #     "expected_output": (
    #         "Remote work is permitted subject to company requirements, business needs, "
    #         "and manager approval."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "REMOTE WORK POLICY\n\n"
    #             "Purpose\n\n"
    #             "This policy establishes guidelines for employees who work remotely "
    #             "or use a hybrid work arrangement.\n\n"
    #             "Eligibility\n\n"
    #             "Remote work eligibility depends on:\n\n"
    #             "Job responsibilities\n"
    #             "Team requirements\n"
    #             "Business needs\n"
    #             "Manager approval\n"
    #             "Employee performance and reliability\n\n"
    #             "Not all roles are suitable for remote work."
    #         )
    #     ],
    # },

    # {
    #     "input": "Can I claim this expense?",
    #     "expected_output": (
    #         "An expense may be claimed if it is an approved business expense "
    #         "incurred during official company activities and meets the reimbursement "
    #         "requirements."
    #     ),
    #     "expected_retrieval_context": [
    #         (
    #             "Eligible Expenses\n\n"
    #             "Reasonable and necessary expenses incurred for legitimate business "
    #             "purposes may be reimbursable.\n\n"
    #             "Examples include:\n\n"
    #             "Business travel\n"
    #             "Transportation\n"
    #             "Accommodation\n"
    #             "Business meals\n"
    #             "Client or business meetings\n"
    #             "Approved conferences and events\n"
    #             "Other expenses specifically authorized by the company"
    #         )
    #     ],
    # },
]
