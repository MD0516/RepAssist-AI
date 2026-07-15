export const formatTime = (
  value,
  {
    showDate = true,
    showTime = false,
    locale = "en-IN",
  } = {}
) => {
  if (!value) return "";

  const date = new Date(value);

  const options = {};

  if (showDate) {
    options.day = "2-digit";
    options.month = "short";
    options.year = "numeric";
  }

  if (showTime) {
    options.hour = "2-digit";
    options.minute = "2-digit";
    options.hour12 = true;
  }

  return new Intl.DateTimeFormat(locale, options).format(date);
};