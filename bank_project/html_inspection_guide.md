# 🔍 HTML Table Inspection Guide

## Steps to Inspect HTML Table Structure:

### 1. **Open the Webpage**
- Navigate to the target webpage in your browser
- For banks: https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks
- For GDP: https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29
- For movies: https://web.archive.org/web/20230126232938/https://www.imdb.com/chart/top/

### 2. **Open Developer Tools**
- **Chrome/Edge**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
- **Firefox**: Press `F12` or `Ctrl+Shift+I` (Windows) / `Cmd+Option+I` (Mac)
- **Safari**: Press `Cmd+Option+I` (Mac)

### 3. **Locate the Table**
- Click the **"Elements"** or **"Inspector"** tab
- Use `Ctrl+F` (Windows) / `Cmd+F` (Mac) to search for:
  - `<table` (finds table elements)
  - `class="wikitable"` (for Wikipedia tables)
  - The table you want to inspect

### 4. **Expand the First Row**
- Find the `<table>` element
- Look for the first `<tr>` (table row) element
- Click the **triangle/arrow** next to `<tr>` to expand it
- You should see the `<td>` (table data) or `<th>` (table header) elements

### 5. **What You Should See:**
```html
<table class="wikitable sortable">
  <tbody>
    <tr>  ← Click this triangle to expand
      <td>Bank Name</td>  ← First column
      <td>Market Cap</td>  ← Second column
      <td>...</td>        ← Other columns
    </tr>
    <tr>...</tr>  ← Additional rows
  </tbody>
</table>
```

### 6. **Take Screenshot**
- Make sure the first `<tr>` is expanded showing all `<td>` elements
- The HTML structure should be visible in the Elements panel
- Take a screenshot that includes both the webpage and the developer tools

## 🎯 Expected HTML Structure for Different Tables:

### **Banks Table:**
```html
<table class="wikitable sortable">
  <tr>
    <td>JPMorgan Chase</td>
    <td>432.92</td>
    <td>...</td>
  </tr>
</table>
```

### **GDP Table:**
```html
<table class="wikitable sortable">
  <tr>
    <td>United States</td>
    <td>26,854,599</td>
    <td>...</td>
  </tr>
</table>
```

### **Movies Table:**
```html
<table>
  <tr>
    <td>1.</td>
    <td>The Shawshank Redemption</td>
    <td>9.3</td>
    <td>1994</td>
  </tr>
</table>
``` 