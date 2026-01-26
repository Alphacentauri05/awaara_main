"use client";

import { useState } from "react";
import UploadForm from "@/components/UploadForm";
import ResultsGrid from "@/components/ResultsGrid";

// Because obviously you can't infer types yourself
interface Match {
    imageUrl: string;
    score: number;
}

export default function Home() {
    const [matches, setMatches] = useState<Match[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (file: File) => {
        setLoading(true);
        setError(null);
        setMatches([]);

        try {
            const formData = new FormData();
            formData.append("file", file);

            const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

            const response = await fetch(`${backendUrl}/find`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || "Of course something went wrong. Try again.");
            }

            const data = await response.json();

            if (data.matches && data.matches.length > 0) {
                setMatches(data.matches);
            } else {
                setError("Apparently you don't exist in these photos. Tragic.");
            }
        } catch (err) {
            setError(err instanceof Error ? err.message : "Of course something went wrong. Try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 flex items-center justify-center p-4">
            <div className="w-full max-w-4xl">
                {/* Main card - because you need everything centered and pretty */}
                <div className="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl shadow-2xl border border-gray-700 p-8 md:p-12">
                    {/* Header */}
                    <div className="text-center mb-8">
                        <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-purple-400 to-pink-600 bg-clip-text text-transparent mb-4">
                            Find My Photos
                        </h1>
                        <p className="text-gray-400 text-lg md:text-xl">
                            Because you can't find your own face in a crowd.
                        </p>
                    </div>

                    {/* Upload form - the only thing you'll interact with */}
                    {!loading && matches.length === 0 && (
                        <UploadForm onSubmit={handleSubmit} />
                    )}

                    {/* Loading state - watching paint dry would be more exciting */}
                    {loading && (
                        <div className="text-center py-12">
                            <div className="inline-block animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-purple-500 mb-4"></div>
                            <p className="text-gray-400">Searching for your face... this might take a while.</p>
                        </div>
                    )}

                    {/* Error state - inevitable */}
                    {error && !loading && (
                        <div className="text-center py-8">
                            <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-6 mb-6">
                                <p className="text-red-400 text-lg">{error}</p>
                            </div>
                            <button
                                onClick={() => {
                                    setError(null);
                                    setMatches([]);
                                }}
                                className="px-6 py-3 bg-purple-600 hover:bg-purple-700 rounded-lg font-medium transition-colors"
                            >
                                Try Again (If You Dare)
                            </button>
                        </div>
                    )}

                    {/* Results - assuming anything actually works */}
                    {!loading && matches.length > 0 && (
                        <div>
                            <div className="mb-6 text-center">
                                <p className="text-gray-300 text-lg">
                                    Found {matches.length} photo{matches.length !== 1 ? 's' : ''} with your face.
                                    Congratulations, you exist.
                                </p>
                                <button
                                    onClick={() => setMatches([])}
                                    className="mt-4 px-6 py-3 bg-gray-700 hover:bg-gray-600 rounded-lg font-medium transition-colors"
                                >
                                    Search Again
                                </button>
                            </div>
                            <ResultsGrid matches={matches} />
                        </div>
                    )}
                </div>

                {/* Footer - legally required pessimism */}
                <p className="text-center text-gray-600 text-sm mt-6">
                    No guarantees this actually works. Built with minimal enthusiasm.
                </p>
            </div>
        </main>
    );
}
