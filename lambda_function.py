import json
import requests
import os

SUPERSET_DOMAIN = os.environ.get('SUPERSET_DOMAIN')
AUTH_TOKEN = os.environ.get('SUPERSET_AUTH_TOKEN')

def lambda_handler(event, context):
    try:
        # Expect input JSON in the 'body' of the API Gateway request
        if 'body' in event:
            input_data = json.loads(event['body'])
        else:
            input_data = event  # For direct testing without API Gateway

        report_data = input_data.get("Report", {})
        superset_data = input_data.get("ReportTypeSuperset", {})
        filters_data = input_data.get("ReportIncludeFilters", [])
        split_dimension_id = input_data.get("SplitDimentionId")
        report_drawer_ids = input_data.get("ReportDrawerIds", [])

        # Build payload based on input
        payload = {
            "nameOfFile": report_data.get("ReportName"),
            "typeOfPage": superset_data.get("PageSize"),
            "orientation": superset_data.get("PageOrientation"),
            "time_range": {
                "start_date": report_data.get("StartDate"),
                "end_date": report_data.get("EndDate")
            },
            "optional_data": {
                "heading": superset_data.get("Header"),
                "subHeading": superset_data.get("SubHeader"),
                # "print_date": input_data.get(""), # CHECK
                "start_date": report_data.get("StartDate"), # CHECK
                "end_date": report_data.get("EndDate"), # CHECK
                "logo": superset_data.get("LogoId"),
            },
            "filters": input_data.get("filters", [
                {
                    # "key": filters_data.get(""),
                    "value": filters_data.get("SelectedValue"),
                    "datasetId": filters_data.get("DimentionId"),
                    "op": filters_data.get("FilterOperator")
                }
            ])
        }

        # Prepare headers with authorization
        headers = {
            "Authorization": AUTH_TOKEN,
            "Content-Type": "application/json"
        }

        # Call Superset API
        SUPERSET_API_URL = f"{SUPERSET_DOMAIN}/dashboard/{report_data.get("ExternalId")}/export_pdf"  # Dashboard Id?
        response = requests.post(SUPERSET_API_URL, headers=headers, json=payload)

        # Return API response
        return {
            "statusCode": response.status_code,
            "body": json.dumps({
                "message": "Report request sent.",
                "superset_response": response.json()
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
