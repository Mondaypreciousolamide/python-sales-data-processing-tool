import csv
from pathlib import Path


def read_sales_data():
    sales_data = []

    with open("data/sales.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            sales_data.append(row)

    return sales_data


def validate_sale(sale):
    if not sale["customer_name"]:
        return False, "Customer name is missing"

    if not sale["product"]:
        return False, "Product name is missing"

    try:
        quantity = int(sale["quantity"])
        price = float(sale["price"])
    except ValueError:
        return False, "Quantity or price is not a valid number"

    if quantity <= 0:
        return False, "Quantity must be greater than 0"

    if price < 0:
        return False, "Price cannot be negative"

    return True, ""


def calculate_total_sales(sales_data):
    total_sales = 0

    for sale in sales_data:
        quantity = int(sale["quantity"])
        price = float(sale["price"])

        sale_total = quantity * price
        total_sales += sale_total

    return total_sales


def generate_report(valid_sales, invalid_sales, total_sales):
    report = []

    report.append("SALES REPORT")
    report.append("============")
    report.append("")
    report.append(f"Valid records: {len(valid_sales)}")
    report.append(f"Invalid records: {len(invalid_sales)}")
    report.append("")
    report.append("Sales details:")
    report.append("")

    for sale in valid_sales:
        quantity = int(sale["quantity"])
        price = float(sale["price"])
        sale_total = quantity * price

        report.append(
            f"{sale["customer_name"]} - "
            f"{sale["product"]} - "
            f"${sale_total:,.2f}"
        )

    report.append("")
    report.append("Invalid records:")
    report.append("")

    for sale, reason in invalid_sales:
        report.append(f"Customer: {sale["customer_name"]}")
        report.append(f"Product: {sale["product"]}")
        report.append(f"Quantity: {sale["quantity"]}")
        report.append(f"Reason: {reason}")
        report.append("")

    report.append(f"Total sales: ${total_sales:,.2f}")
    report.append("")

    Path("reports/sales_report.txt").write_text(
        "\n".join(report),
        encoding="utf-8"
    )


def main():
    sales_data = read_sales_data()

    valid_sales = []
    invalid_sales = []

    for sale in sales_data:
        is_valid, reason = validate_sale(sale)

        if is_valid:
            valid_sales.append(sale)
        else:
            invalid_sales.append((sale, reason))

    total_sales = calculate_total_sales(valid_sales)

    print("Valid records:", len(valid_sales))

    print()
    print("Sales details:")

    for sale in valid_sales:
        quantity = int(sale["quantity"])
        price = float(sale["price"])
        sale_total = quantity * price

        print(f"{sale["customer_name"]} - {sale["product"]} - ${sale_total:.2f}")
    print("Invalid records:", len(invalid_sales))

    for sale, reason in invalid_sales:
        print()
        print("Invalid record:")
        print("Customer:", sale["customer_name"])
        print("Product:", sale["product"])
        print("Quantity:", sale["quantity"])
        print("Reason:", reason)

    print()
    print(f"Total sales: ${total_sales:,.2f}")

    generate_report(valid_sales, invalid_sales, total_sales)


main()
