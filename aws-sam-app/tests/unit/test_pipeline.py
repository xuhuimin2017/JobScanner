from pathlib import Path

from pipeline import Pipeline

test_root = (Path(__file__).parent / '..').resolve().absolute()
resume_data = test_root / 'resumes'


def test_from_cv_pdf():
    cv1 = resume_data / 'cv1.pdf'
    assert cv1.is_file(), f'Test file not exist "{cv1}"'

    pipe = Pipeline().load()

    # Get text from pdf
    cv_text = pipe.cv_from_pdf(str(cv1))
    assert cv_text

    jobs, skills, = pipe.get_job_recommendations(cv_text)
    assert len(jobs) > 0
    assert len(skills) > 0

