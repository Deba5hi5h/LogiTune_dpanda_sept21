class Comparator:
    @staticmethod
    def compare_versions(version_first: str, version_second: str) -> int:
        """Compares two strings versions and returns:

        1 if first is greater

        2 if second is greater

        0 if versions are equal

        greater.
        """
        first_split, second_split = [el.split('.') for el in (version_first, version_second)]

        # Add 0 if versions lengths differ
        while len(first_split) != len(second_split):
            if len(first_split) > len(second_split):
                second_split.append('0')
            else:
                first_split.append('0')

        zipped = tuple(zip(first_split, second_split))
        # Check if equal
        if all(int(el[0]) == int(el[1]) for el in zipped):
            return 0

        # Check if greater or lower
        for el in zipped:
            if int(el[0]) > int(el[1]):
                return 1
            elif int(el[0]) == int(el[1]):
                continue
            else:
                return 2


if __name__ == "__main__":
    res = Comparator.compare_versions('8.13.1', '8.2.3')
    print(res)
