from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    filename,
    name,
    email,
    phone,
    score,
    rating,
    missing,
    recommendations
):

    pdf_file = "ATS_Report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Resume Screening Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            f"Name: {name}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Email: {email}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Phone: {phone}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Resume: {filename}",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Match Score: {score}%",
            styles["BodyText"]
        )
    )

    content.append(
        Paragraph(
            f"Rating: {rating}",
            styles["BodyText"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Missing Skills",
            styles["Heading2"]
        )
    )

    for skill in missing:
        content.append(
            Paragraph(
                f"• {skill}",
                styles["BodyText"]
            )
        )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "ATS Recommendations",
            styles["Heading2"]
        )
    )

    for item in recommendations:
        content.append(
            Paragraph(
                f"• {item}",
                styles["BodyText"]
            )
        )

    doc.build(content)

    return pdf_file