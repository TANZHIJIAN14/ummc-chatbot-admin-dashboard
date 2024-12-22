# Custom CSS to control column widths
custom_css = """
#dataframe-container table {
    table-layout: fixed; /* Ensures the table respects column width settings */
    width: 100%;         /* Table occupies full width */
}
#dataframe-container th:nth-child(1), #dataframe-container td:nth-child(1) {
    width: 150px; /* Width for the first column (_id) */
}
#dataframe-container th:nth-child(2), #dataframe-container td:nth-child(2) {
    width: 150px; /* Width for the second column (user_id) */
}
#dataframe-container th:nth-child(3), #dataframe-container td:nth-child(3) {
    width: 300px; /* Width for the third column (message) */
    white-space: pre-wrap;  /* Allow breaking lines */
    overflow: hidden;       /* Hide overflow */
    text-overflow: ellipsis;/* Add ellipsis if needed */
    max-width: 300px;       /* Set a maximum width */
    word-wrap: break-word;  /* Break long words */
}
#dataframe-container th:nth-child(4), #dataframe-container td:nth-child(4) {
    width: 150px; /* Width for the fourth column (created_at) */
}
"""