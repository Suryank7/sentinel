import "./globals.css";

export const metadata = {
  title: "SENTINEL - Safety Command Centre",
  description: "AI-Powered Industrial Safety Intelligence",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <div id="root">
          {children}
        </div>
      </body>
    </html>
  );
}
