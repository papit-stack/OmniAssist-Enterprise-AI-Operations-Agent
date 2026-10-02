test_cases = [

    # =========================
    # Company Overview
    # =========================

    {
        "input": "When was NovaTech Solutions founded and how many employees does it have?",
        "expected_output": (
            "NovaTech Solutions Private Limited was founded in 2014 by two co-founders "
            "and has approximately 1,200 employees as of 2025. It is a technology "
            "company that designs and builds software products and provides IT services "
            "to clients across banking, healthcare, and retail industries."
        ),
        "expected_retrieval_context": [
            (
                "NovaTech Solutions Private Limited (NovaTech) is a technology company founded in 2014. "
                "We design and build software products and provide IT services. Today the company has "
                "more than 1,200 employees and serves clients across banking, healthcare, and retail industries.\n\n"
                "Employees: approximately 1,200 as of 2025.\n"
                "Revenue: annual revenue of approximately USD 45 million.\n"
                "Founded: 2014 by two co-founders. Profitable since 2018.\n"
                "Employer of Choice: listed among the \"Best IT Workplaces\" in India for 2024."
            )
        ],
    },

    # =========================
    # Leave Policy
    # =========================

    {
        "input": "How many days of earned leave and casual leave do I get per year?",
        "expected_output": (
            "You get 18 days of Earned Leave (EL) per year, which is eligible after completing "
            "6 months of service, and 8 days of Casual Leave (CL) per year. Casual leave cannot "
            "be carried forward; only Earned Leave of up to 30 days can be carried forward to the next year."
        ),
        "expected_retrieval_context": [
            (
                "1. Earned Leave (EL): 18 days per year. Eligible after completing 6 months of service. "
                "Can be encashed up to a maximum of 5 days per year. Unused EL of up to 30 days can be "
                "carried forward to the next year.\n"
                "2. Casual Leave (CL): 8 days per year. Meant for short, unplanned absences. "
                "Cannot be carried forward. At least 1 day advance notice is expected unless it is an emergency."
            )
        ],
    },

    # =========================
    # Employee Benefits
    # =========================

    {
        "input": "What is the medical insurance cover at NovaTech?",
        "expected_output": (
            "NovaTech provides group medical insurance of INR 8,00,000 per employee per year for "
            "self, spouse, and up to 2 dependent children through a top insurance partner. "
            "Employees can voluntarily cover parents by paying a small premium."
        ),
        "expected_retrieval_context": [
            (
                "1. Group Medical Insurance: Cover of INR 8,00,000 per employee per year for self, "
                "spouse, and up to 2 dependent children. Provided through a top insurance partner. "
                "Employees can also voluntarily cover parents by paying a small premium."
            )
        ],
    },

    # =========================
    # HR Policies and Onboarding
    # =========================

    {
        "input": "How long is the probation period and the notice period for a regular employee?",
        "expected_output": (
            "Every new employee has a probation period of 6 months, extendable by a maximum of "
            "3 months. The notice period is 60 days for regular employees (or buy-out at management "
            "discretion) and 15 days during probation."
        ),
        "expected_retrieval_context": [
            (
                "Every new employee has a probation period of 6 months, extendable by a maximum of "
                "3 months. During probation, regular feedback is given. Confirmation is subject to "
                "satisfactory performance. No leave encashment is applicable during probation.\n\n"
                "- Notice period for regular employees: 60 days, or buy-out at management discretion.\n"
                "- Notice period during probation: 15 days."
            )
        ],
    },

    # =========================
    # Payroll and Compensation
    # =========================

    {
        "input": "When is salary paid each month?",
        "expected_output": (
            "Salary is paid on the last working day of every month for the completed month. "
            "If that date falls on a weekend or a public holiday, salary is credited on the "
            "immediately preceding working day."
        ),
        "expected_retrieval_context": [
            (
                "Salary is paid on the last working day of every month, i.e., the last working day "
                "of the calendar month, for the completed month. If the date falls on a weekend or a "
                "public holiday, salary is credited on the immediately preceding working day."
            )
        ],
    },

    # =========================
    # Office and Facilities
    # =========================

    {
        "input": "What are the office timings and how do I book a meeting room?",
        "expected_output": (
            "Standard office hours are 9:00 AM to 6:00 PM, Monday to Friday, with flexi timing "
            "between 8:00 AM and 8:00 PM available with manager approval. Meeting rooms can be "
            "booked through the calendar system up to 2 weeks in advance."
        ),
        "expected_retrieval_context": [
            (
                "- Standard office hours: 9:00 AM to 6:00 PM, Monday to Friday.\n"
                "- Offices remain open from 8:00 AM to 8:00 PM for flexi timing with manager approval.\n\n"
                "3. Meeting Rooms: Book through the calendar system up to 2 weeks in advance; "
                "video-conferencing enabled."
            )
        ],
    },

    # =========================
    # IT and Security Policy
    # =========================

    {
        "input": "What is the password requirement for company accounts?",
        "expected_output": (
            "Passwords must be at least 12 characters and include upper case, lower case, numbers, "
            "and special characters. Passwords must be changed every 90 days and you must never "
            "reuse the last 5 passwords. All company accounts must also use Multi-Factor Authentication (MFA)."
        ),
        "expected_retrieval_context": [
            (
                "- All company accounts must use Multi-Factor Authentication (MFA). Set up MFA on day 1 "
                "for your email and SSO accounts.\n"
                "- Passwords must be at least 12 characters and include upper case, lower case, numbers, "
                "and special characters.\n"
                "- Passwords must be changed every 90 days. Never reuse the last 5 passwords."
            )
        ],
    },

    # =========================
    # Travel and Expense Policy
    # =========================

    {
        "input": "How much is the daily allowance for domestic travel?",
        "expected_output": (
            "For domestic travel, the per diem is INR 900 per day toward food and incidental expenses. "
            "No receipt is needed for per diem up to 6 hours (half-day); full-day rules apply as per the portal. "
            "Claims must be pre-approved where applicable and submitted within 30 days."
        ),
        "expected_retrieval_context": [
            (
                "- Domestic travel: INR 900 per day toward food and incidental expenses. No receipt needed "
                "for per diem up to 6 hours (half-day) and full-day rules apply as per portal.\n"
                "- International travel: The per diem differs by country and is published on the travel page."
            )
        ],
    },

    # =========================
    # Performance and Promotions
    # =========================

    {
        "input": "What is the minimum tenure required for a promotion?",
        "expected_output": (
            "To be eligible for a promotion you need a minimum of 18 months in your current role at "
            "the time of the review cycle, or 12 months for outstanding performers. Promotion is based "
            "on ratings (last 2 cycles average 4 or above), skills, and business need, and is approved "
            "by a promotion committee."
        ),
        "expected_retrieval_context": [
            (
                "- Eligibility: minimum 18 months in current role at the time of review cycle "
                "(12 months for outstanding performers).\n"
                "- Promotion is based on ratings (last 2 cycles average 4 or above), skills, and business need. "
                "A promotion committee approves all promotions."
            )
        ],
    },

    # =========================
    # Learning and Development
    # =========================

    {
        "input": "How much is the yearly learning budget for an employee?",
        "expected_output": (
            "Every employee gets a learning budget of INR 25,000 per year for courses, books, "
            "certifications, and conferences. The budget covers the full cost of work-related training "
            "and unused budget does not carry forward. Courses must be approved by the manager "
            "through Employee Portal > Learning > Course Request."
        ),
        "expected_retrieval_context": [
            (
                "- INR 25,000 per year for every employee on courses, books, certifications, and conferences.\n"
                "- The budget covers the full cost of work-related training. Unused budget does not carry forward.\n"
                "- Courses must be approved by the manager. Requests are made through Employee Portal > "
                "Learning > Course Request."
            )
        ],
    },
]