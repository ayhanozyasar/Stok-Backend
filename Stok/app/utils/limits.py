def apply_plan_limits(company):
    if company.plan == "free":
        company.max_users = 2
        company.max_products = 10

    elif company.plan == "pro":
        company.max_users = 10
        company.max_products = 100