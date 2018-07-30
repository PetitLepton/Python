<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />

<style type="text/css">

@import url('https://fonts.googleapis.com/css?family=IBM+Plex+Serif:400,400i');
@import url('https://fonts.googleapis.com/css?family=IBM+Plex+Sans:400');
@import url('https://fonts.googleapis.com/css?family=IBM+Plex+Sans+Condensed:400,600');
@import url('https://fonts.googleapis.com/css?family=IBM+Plex+Mono:400');


/* Overrides of notebook CSS for static HTML export */
body {
  overflow: visible;
  margin: 0 auto;
  margin-left: 10%;
  font-family :  'IBM Plex Serif', sans-serif;
  font-weight: 400;
  font-size: 17px;
  line-height: 1.6;
  font-variant-ligatures: common-ligatures;
  font-variant-numeric: oldstyle-nums;
  -moz-font-feature-settings: "liga", "clig", "onum";
  -webkit-font-feature-settings: "liga", "clig", "onum";
  font-feature-settings: "liga", "clig", "onum";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3, h4 {
  font-family: 'IBM Plex Sans Condensed';
  text-transform: uppercase;
  line-height: 1.2;
  font-weight: 600;
  max-width: 30ch;
}
h1 {font-size: 2.441em;}
h2 {font-size: 1.953em;}
h3 {font-size: 1.563em;}
h4 {font-size: 1.25em;}


p, ul {
    max-width: 70ch;
}
blockquote {
  font-size: 0.8em;
}

img {
    max-width: 100%;
    max-height: 30ex;
}

table {
    color: #000000;
    font-weight: 400;
    font-family: 'IBM Plex Mono', monospace;
    border: 0px;
    border-spacing: 0px;
    border-collapse: collapse;
    margin-bottom: 1em;
    margin-right: 1em; /* when outputs are on a row */
}

th, tr, td {
  font-size: 0.8em;
  font-weight: 400;
  border: 1px solid #efecea;
  padding-left: 0.5em;
  padding-right: 0.5em;
  overflow-wrap: break-word;
}

thead th {
  font-family: 'IBM Plex Sans';
  font-size: 1em;
  background-color: #efecea;
}

thead tr th, tbody tr th {
    text-align: left;
}

tbody tr td {
    text-align: right;
}

th.index_name, th.row_heading {
  text-align: left;
}

/* This is related to code */
code {
  /* color: #4e79a7; */
  font-family: 'IBM Plex Mono', monospace;
}
pre {
  /* color: #4e79a7; */
  font-family: 'IBM Plex Mono', monospace;
  font-size: 0.8em;
}

/*This one is related to the link at the end of the header. */
.anchor-link {
  display: none;
}

/* HTML links*/
a {
  color: #4e79a7;
  text-decoration: none;
}

button {
  font-family : inherit;
  font-weight: inherit;
  font-size: inherit;
  border-style: none;
  background-color: #efecea;
  color: #635f5d;
}


</style>
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.12.0/build/styles/github-gist.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@9.12.0/build/highlight.min.js"></script>
<script>hljs.initHighlightingOnLoad();</script>
</head>

<body>
    {{ content }}
</body>
</html>
