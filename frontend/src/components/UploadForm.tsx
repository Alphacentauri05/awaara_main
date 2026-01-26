"use client";

import { useState, useRef } from "react";
import Image from "next/image";

interface UploadFormProps {
    onSubmit: (file: File) => void;
}

export default function UploadForm({ onSubmit }: UploadFormProps) {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            // Basic validation because you'll probably try to upload a PDF
            if (!file.type.startsWith("image/")) {
                alert("That's not an image. Try again with an actual photo.");
                return;
            }

            setSelectedFile(file);

            // Create preview URL
            const url = URL.createObjectURL(file);
            setPreviewUrl(url);
        }
    };

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();

        if (!selectedFile) {
            alert("You forgot to select a file. Predictable.");
            return;
        }

        onSubmit(selectedFile);
    };

    const handleReset = () => {
        setSelectedFile(null);
        if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
            setPreviewUrl(null);
        }
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            {/* File input area - make it obvious enough even for you */}
            <div className="relative">
                <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    onChange={handleFileSelect}
                    className="hidden"
                    id="file-upload"
                />

                <label
                    htmlFor="file-upload"
                    className="block cursor-pointer"
                >
                    <div className="border-2 border-dashed border-gray-600 hover:border-purple-500 rounded-xl p-8 text-center transition-colors bg-gray-800/50 hover:bg-gray-800">
                        {!selectedFile ? (
                            <>
                                <svg
                                    className="mx-auto h-16 w-16 text-gray-500 mb-4"
                                    fill="none"
                                    viewBox="0 0 24 24"
                                    stroke="currentColor"
                                >
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        strokeWidth={2}
                                        d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                                    />
                                </svg>
                                <p className="text-gray-400 text-lg mb-2">
                                    Click to upload your selfie
                                </p>
                                <p className="text-gray-600 text-sm">
                                    One photo. Your face. Don't overthink it.
                                </p>
                            </>
                        ) : (
                            <div className="space-y-4">
                                {previewUrl && (
                                    <div className="relative w-48 h-48 mx-auto rounded-lg overflow-hidden">
                                        <Image
                                            src={previewUrl}
                                            alt="Preview"
                                            fill
                                            className="object-cover"
                                        />
                                    </div>
                                )}
                                <p className="text-gray-300 font-medium">{selectedFile.name}</p>
                                <p className="text-gray-500 text-sm">
                                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                                </p>
                            </div>
                        )}
                    </div>
                </label>
            </div>

            {/* Action buttons - because you need hand-holding */}
            {selectedFile && (
                <div className="flex gap-4">
                    <button
                        type="submit"
                        className="flex-1 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-semibold py-4 px-6 rounded-lg transition-all transform hover:scale-105 shadow-lg"
                    >
                        Search My Face
                    </button>
                    <button
                        type="button"
                        onClick={handleReset}
                        className="px-6 py-4 bg-gray-700 hover:bg-gray-600 text-white font-semibold rounded-lg transition-colors"
                    >
                        Cancel
                    </button>
                </div>
            )}
        </form>
    );
}
