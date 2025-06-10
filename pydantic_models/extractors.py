class FieldExtractor:
    def _sum_with_fallback(
        self,
        df,
        primary_col,
        fallback_col,
        fallback_transform=lambda x: x
    ):
        if primary_col in df.columns:
            return df[primary_col].sum()
        elif fallback_col in df.columns:
            return fallback_transform(df[fallback_col]).sum()
        return 0.0
