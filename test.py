def add_binary_numbers(first: str, second: str) -> str:
	"""Return the sum of two binary numbers represented as strings."""
	return bin(int(first, 2) + int(second, 2))[2:]


if __name__ == "__main__":
	print(add_binary_numbers("1011", "1101"))  # 11000
