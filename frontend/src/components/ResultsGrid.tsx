"use client";

import Image from "next/image";

interface Match {
    imageUrl: string;
    score: number;
}

interface ResultsGridProps {
    matches: Match[];
}

export default function ResultsGrid({ matches }: ResultsGridProps) {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {matches.map((match, index) => (
                <div
                    key={index}
                    className="relative group overflow-hidden rounded-lg bg-gray-800 border border-gray-700 hover:border-purple-500 transition-all hover:scale-105"
                >
                    {/* Image container */}
                    <div className="relative aspect-square">
                        <Image
                            src={match.imageUrl}
                            alt={`Match ${index + 1}`}
                            fill
                            className="object-cover"
                            sizes="(max-width: 640px) 100vw, (max-width: 768px) 50vw, 33vw"
                        />

                        {/* Overlay with score - appears on hover because subtle is better */}
                        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                            <div className="absolute bottom-0 left-0 right-0 p-4">
                                <div className="flex items-center justify-between">
                                    <span className="text-sm text-gray-300">Similarity</span>
                                    <span className="text-lg font-bold text-purple-400">
                                        {(match.score * 100).toFixed(1)}%
                                    </span>
                                </div>

                                {/* Progress bar because visual feedback is important */}
                                <div className="mt-2 h-1 bg-gray-700 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all"
                                        style={{ width: `${match.score * 100}%` }}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Download link because you'll want to save these */}
                    <a
                        href={match.imageUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="absolute top-2 right-2 bg-black/60 hover:bg-black/80 p-2 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                        title="Open full image"
                    >
                        <svg
                            className="w-5 h-5 text-white"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                            />
                        </svg>
                    </a>
                </div>
            ))}
        </div>
    );
}
