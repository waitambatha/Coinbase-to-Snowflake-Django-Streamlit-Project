import snowflake.connector
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from dotenv import load_dotenv
# Load environment variables from the .env file located in the project root
load_dotenv()

# Retrieve Snowflake credentials from the environment variables
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")



def get_snowflake_data():
    """Connect to Snowflake, select all columns from CURRENCIES, and return as a list of dictionaries."""
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    cs = conn.cursor()
    try:
        cs.execute("SELECT * FROM CURRENCIES")
        # Get column names (they are returned as uppercase by default)
        col_names = [desc[0] for desc in cs.description]
        rows = cs.fetchall()
        result = []
        for row in rows:
            row_dict = dict(zip(col_names, row))
            result.append(row_dict)
        return result
    finally:
        cs.close()
        conn.close()


# -------------------------
# Existing API views here...
# (Level1Currencies, Level2Currencies, Level3Currencies, etc.)
# -------------------------

@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    # No authentication or permissions are required for login
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"detail": "Login successful."})
        else:
            return Response({"detail": "Invalid credentials."},
                            status=status.HTTP_400_BAD_REQUEST)

# --- API Views with Updated Data Levels ---

class Level1Currencies(APIView):
    permission_classes = [AllowAny]  # Public access

    def get(self, request):
        data = get_snowflake_data()
        # For Level 1, show only minimal fields (for example, only ID and STATUS)
        filtered_data = []
        for d in data:
            filtered_data.append({
                "ID": d.get("ID"),  # from the CSV, original JSON "id" became "ID"
                "STATUS": d.get("STATUS")  # e.g., "online"
            })
        streamlit_link = "http://localhost:8501/level1"
        return Response({
            "data": filtered_data,
            "visualization": streamlit_link
        })


class Level2Currencies(APIView):
    permission_classes = [IsAuthenticated]  # Authenticated users only

    def get(self, request):
        data = get_snowflake_data()
        # For Level 2, return a moderate subset of fields:
        # e.g., ID, NAME, MIN_SIZE, STATUS, DEFAULT_NETWORK, DISPLAY_NAME
        filtered_data = []
        for d in data:
            filtered_data.append({
                "ID": d.get("ID"),
                "NAME": d.get("NAME"),
                "MIN_SIZE": d.get("MIN_SIZE"),
                "STATUS": d.get("STATUS"),
                "DEFAULT_NETWORK": d.get("DEFAULT_NETWORK"),
                "DISPLAY_NAME": d.get("DISPLAY_NAME")
            })
        streamlit_link = "http://localhost:8502/level2"
        return Response({
            "data": filtered_data,
            "visualization": streamlit_link
        })


class Level3Currencies(APIView):
    permission_classes = [IsAdminUser]  # Admin users only

    def get(self, request):
        data = get_snowflake_data()
        # For Level 3, return all columns
        streamlit_link = "http://localhost:8503/level3"
        return Response({
            "data": data,
            "visualization": streamlit_link
        })
