from hudson_utils.args import get_from_args


def test_get_from_args_found():
    args = ["--threshold=0.7", "--other=option"]
    result = get_from_args(args, "threshold", "0.5")
    assert result == "0.7"


def test_get_from_args_not_found():
    args = ["--other=option"]
    result = get_from_args(args, "threshold", "0.5")
    assert result == "0.5"


def test_get_from_args_empty_args():
    args = []
    result = get_from_args(args, "threshold", "0.5")
    assert result == "0.5"


def test_get_from_args_multiple_args():
    args = ["--threshold=0.7", "--threshold=0.8"]
    result = get_from_args(args, "threshold", "0.5")
    assert result == "0.7"


def test_get_from_args_no_default():
    args = ["--threshold=0.7"]
    result = get_from_args(args, "threshold", default_value=None)
    assert result == "0.7"
