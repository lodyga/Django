def validate_find_unique_binary_string(output, nums):
    return (
        len(output) == len(nums[0])
        and set(output) <= {"0", "1"}
        and output not in nums
    )
