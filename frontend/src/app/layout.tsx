import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "Find My Photos | Because You Can't Find Yourself",
    description: "Upload a selfie and we'll find you in event photos. Assuming you were actually there.",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <body className="antialiased">{children}</body>
        </html>
    );
}
