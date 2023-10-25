def assessment_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)

        except Exception as err:
            raise ValueError(f'Something went wrong in the assessment: {err}')
            

    return wrapper

