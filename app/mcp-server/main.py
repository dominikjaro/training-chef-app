from fastmcp import FastMCP

# No Gemini here! Just tools.
server = FastMCP(name="Training Chef Tools")

@server.tool()
def get_strava_stats(user_id: str) -> str:
    """
    Fetches the user's recent ride statistics from Strava.
    """
    # Later you will add real Strava API code here
    return f"User {user_id} rode 150km this week with 2000m elevation gain."

if __name__ == "__main__":
    # Listen on all interfaces so K8s can reach it
    server.run(transport="sse", port=8080, host="0.0.0.0")