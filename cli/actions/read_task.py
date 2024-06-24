from notion.client import query

def run(args):
    # Create the filter object
    filters = {
        "and": []
    }

    # Helper function to add filters
    def add_filter(property_name, property_type, values):
        if isinstance(values, list):
            for value in values:
                filters["and"].append({
                    "property": property_name,
                    property_type: {
                        "contains" if property_type == "multi_select" else "equals": value
                    }
                })
        else:
            filters["and"].append({
                "property": property_name,
                property_type: {
                    "equals": values
                }
            })

    # Add filters based on the filter parameters
    if "list" in args.keys():
        add_filter("List", "select", args["list"])

    if "categories" in args.keys():
        add_filter("Categories", "multi_select", args["categories"])

    if "status" in args.keys():
        add_filter("Status", "select", args["status"])

    if "title" in args.keys():
        add_filter("Name", "title", args["title"])
        
    return query("task", filters)