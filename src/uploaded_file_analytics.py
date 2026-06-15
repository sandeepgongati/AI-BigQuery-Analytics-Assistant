import pandas as pd

def load_file(uploaded_file):

    if uploaded_file.name.endswith(".csv"):

        encodings = [
            "utf-8",
            "latin1",
            "cp1252"
        ]

        for encoding in encodings:

            try:

                uploaded_file.seek(0)

                return pd.read_csv(
                    uploaded_file,
                    encoding=encoding,
                    sep=None,
                    engine="python"
                )

            except:
                pass

        raise Exception(
            "Unable to read CSV file."
        )

    elif uploaded_file.name.endswith(".xlsx"):

        return pd.read_excel(uploaded_file)

    else:

        raise Exception(
            "Unsupported file format."
        )


def get_basic_stats(df):

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicates": int(df.duplicated().sum())
    }