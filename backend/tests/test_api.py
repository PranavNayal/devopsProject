from fastapi import status

def test_health(client):
    """Verify liveness probe returns status UP."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "UP"}

def test_ready(client):
    """Verify readiness probe verifies database and returns status READY."""
    response = client.get("/ready")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "READY"}

def test_root(client):
    """Verify root endpoint returns API metadata."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["service"] == "TaskBoard API"
    assert data["version"] == "1.0.0"

def test_create_task(client):
    """Verify creating a new task via POST /api/tasks."""
    payload = {
        "title": "Set up CI/CD pipeline",
        "description": "Configure GitHub Actions and Trivy scan",
        "priority": "HIGH",
        "status": "TODO",
        "assignee": "DevOps Engineer",
    }
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == payload["title"]
    assert data["priority"] == "HIGH"
    assert data["status"] == "TODO"
    assert data["assignee"] == "DevOps Engineer"

def test_list_tasks(client):
    """Verify listing tasks via GET /api/tasks."""
    client.post("/api/tasks", json={"title": "Task 1", "priority": "LOW"})
    client.post("/api/tasks", json={"title": "Task 2", "priority": "MEDIUM"})

    response = client.get("/api/tasks")
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 2"  # descending order
    assert tasks[1]["title"] == "Task 1"

def test_get_task_by_id(client):
    """Verify fetching an individual task by ID."""
    created = client.post("/api/tasks", json={"title": "Specific Task"}).json()
    task_id = created["id"]

    response = client.get(f"/api/tasks/{task_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Specific Task"

def test_get_task_not_found(client):
    """Verify 404 response when querying a non-existent task ID."""
    response = client.get("/api/tasks/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Task not found"

def test_update_task(client):
    """Verify updating a task's status and priority via PUT /api/tasks/{id}."""
    created = client.post("/api/tasks", json={"title": "Initial Title", "status": "TODO"}).json()
    task_id = created["id"]

    update_payload = {"title": "Updated Title", "status": "IN_PROGRESS", "priority": "HIGH"}
    response = client.put(f"/api/tasks/{task_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["status"] == "IN_PROGRESS"
    assert data["priority"] == "HIGH"

def test_stats_endpoint(client):
    """Verify task statistics aggregation via GET /api/tasks/stats."""
    client.post("/api/tasks", json={"title": "T1", "status": "TODO"})
    client.post("/api/tasks", json={"title": "T2", "status": "TODO"})
    client.post("/api/tasks", json={"title": "T3", "status": "IN_PROGRESS"})
    client.post("/api/tasks", json={"title": "T4", "status": "DONE"})

    response = client.get("/api/tasks/stats")
    assert response.status_code == status.HTTP_200_OK
    stats = response.json()
    assert stats["total"] == 4
    assert stats["todo"] == 2
    assert stats["inProgress"] == 1
    assert stats["done"] == 1

def test_delete_task(client):
    """Verify deleting a task via DELETE /api/tasks/{id}."""
    created = client.post("/api/tasks", json={"title": "To be deleted"}).json()
    task_id = created["id"]

    del_resp = client.delete(f"/api/tasks/{task_id}")
    assert del_resp.status_code == status.HTTP_204_NO_CONTENT

    get_resp = client.get(f"/api/tasks/{task_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND
