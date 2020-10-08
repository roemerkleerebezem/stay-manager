module.exports = {
  devServer: {
    proxy: {
      "^/api": {
        logLevel: "debug",
        target: "http://localhost:5000",
        secure: false,
      },
    },
  },
  pages: {
    index: {
      entry: "src/main.js",
      template: "public/index.html",
      filename: "index.html",
      title: "Index Page",
      // chunks to include on this page, by default includes
      // extracted common chunks and vendor chunks.
      chunks: ["chunk-vendors", "chunk-common", "index"],
    },
    // when using the entry-only string format,
    // template is inferred to be `public/subpage.html`
    // and falls back to `public/index.html` if not found.
    // Output filename is inferred to be `subpage.html`.
    htmlinvoice: "src/htmlinvoice.js",
  },
};
