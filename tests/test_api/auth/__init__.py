headers = response.headers
assert headers["filename"] == f"'{test_image_path.name}'"
assert headers["custom-delimiter"] == f"'{delimiter}'"
assert headers["least-significant-bit-amount"] == str(lsb_n)
assert headers["reversed-encoding"] == str(False)
assert headers["message"] == f"'{message}'"
assert headers["content-type"] == "image/png"
assert "test.png" in headers["content-disposition"]


def test_post_msg_too_long(
    api_client: TestClient,
    api_image_file: dict[str, tuple[str, BinaryIO, str]],
) -> None:
    """Test a response with a message longer than allowed."""
    response = api_client.post(
        f"/encode?message={'long-message' * 100}",
        files=api_image_file,
    )

    assert response.status_code == 400
    assert "is not enough for the message (1,200)." in response.content.decode()
    assert "long-message" in response.headers["message"]

    #####

    assert response.status_code == 400
    assert (
        "No message found after scanning the whole image." in response.json()["detail"]
    )

    headers = response.headers
    assert headers["filename"] == f"'{test_image_path.name}'"
    assert headers["custom-delimiter"] == f"'{delimiter}'"
    assert headers["least-significant-bit-amount"] == str(lsb_n)
    assert headers["reversed-encoding"] == str(rev)
    assert headers["content-length"] == str(63)
    assert headers["content-type"] == "application/json"

    json_ = response.json()
    assert response.status_code == 422
    assert json_["field"] == "least-significant-bit-amount"
    assert f"ensure this value is {'greater' if lsb_n < 1 else 'less'}" in json_["info"]
    assert response.headers["content-type"] == "application/json"
