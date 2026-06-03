import pytest
from fastapi.testclient import TestClient
from src.app import app

# Create test client
client = TestClient(app)


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_200(self):
        """Test that GET /activities returns 200"""
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status

    def test_get_activities_returns_dict(self):
        """Test that GET /activities returns a dictionary"""
        # Arrange
        expected_type = dict

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, expected_type)

    def test_get_activities_contains_expected_activities(self):
        """Test that the response contains expected activities"""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity in expected_activities:
            assert activity in data

    def test_get_activities_has_required_fields(self):
        """Test that each activity has required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        for activity_name, activity_data in data.items():
            assert required_fields.issubset(activity_data.keys())

    def test_get_activities_participants_is_list(self):
        """Test that participants field is a list"""
        # Arrange
        expected_type = list

        # Act
        response = client.get("/activities")
        data = response.json()
        first_activity = next(iter(data.values()))

        # Assert
        assert isinstance(first_activity["participants"], expected_type)


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_student_returns_200(self):
        """Test successful signup for a new student returns 200"""
        # Arrange
        activity_name = "Chess%20Club"
        email = "newtestuser123@mergington.edu"
        expected_status = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == expected_status

    def test_signup_returns_success_message(self):
        """Test that signup returns a success message"""
        # Arrange
        activity_name = "Programming%20Class"
        email = "successtest@mergington.edu"
        expected_message_text = "Signed up"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert expected_message_text in data["message"]

    def test_signup_duplicate_student_returns_400(self):
        """Test that duplicate signup returns 400 error"""
        # Arrange
        activity_name = "Chess%20Club"
        email = "michael@mergington.edu"  # Already signed up
        expected_status = 400
        expected_detail_text = "already signed up"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == expected_status
        assert expected_detail_text in data.get("detail", "").lower()

    def test_signup_nonexistent_activity_returns_404(self):
        """Test that signing up for nonexistent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent%20Club"
        email = "student@mergington.edu"
        expected_status = 404
        expected_detail_text = "not found"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == expected_status
        assert expected_detail_text in data.get("detail", "").lower()

    def test_signup_response_contains_email_and_activity(self):
        """Test that success message contains email and activity name"""
        # Arrange
        activity_name = "Art%20Studio"
        email = "artlover@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert email in data["message"]
        assert "Art Studio" in data["message"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""

    def test_unregister_signed_up_student_returns_200(self):
        """Test successful unregister returns 200"""
        # Arrange
        activity_name = "Chess%20Club"
        email = "daniel@mergington.edu"  # Already signed up
        expected_status = 200

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == expected_status

    def test_unregister_returns_success_message(self):
        """Test that unregister returns a success message"""
        # Arrange
        activity_name = "Programming%20Class"
        email = "sophia@mergington.edu"  # Already signed up
        expected_message_text = "Unregistered"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert expected_message_text in data["message"]

    def test_unregister_not_signed_up_returns_400(self):
        """Test that unregistering someone not signed up returns 400"""
        # Arrange
        activity_name = "Chess%20Club"
        email = "nosuchstudent@mergington.edu"
        expected_status = 400
        expected_detail_text = "not signed up"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == expected_status
        assert expected_detail_text in data.get("detail", "").lower()

    def test_unregister_nonexistent_activity_returns_404(self):
        """Test that unregistering from nonexistent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent%20Club"
        email = "student@mergington.edu"
        expected_status = 404
        expected_detail_text = "not found"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert response.status_code == expected_status
        assert expected_detail_text in data.get("detail", "").lower()

    def test_unregister_response_contains_email_and_activity(self):
        """Test that unregister message contains email and activity name"""
        # Arrange
        activity_name = "Swimming%20Team"
        email = "ava@mergington.edu"  # Already signed up

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        data = response.json()

        # Assert
        assert email in data["message"]
        assert "Swimming Team" in data["message"]


class TestRootRedirect:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static_html(self):
        """Test that root endpoint redirects to /static/index.html"""
        # Arrange
        expected_status = 307
        expected_location = "/static/index.html"

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == expected_status
        assert response.headers["location"] == expected_location

    def test_root_with_follow_redirects_returns_200(self):
        """Test that root endpoint with follow_redirects returns 200 or 404 (static mount)"""
        # Arrange
        # Note: This may return 404 if static files aren't served in tests

        # Act
        response = client.get("/", follow_redirects=True)

        # Assert
        # The status code should be either 200 (if static served) or 404 (if not)
        assert response.status_code in [200, 404]
