"use client";

import { useRef, useState } from "react";
import { Camera, Upload, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface DiseaseUploadProps {
  onSelect: (file: File) => void;
  analyzing: boolean;
}

export default function DiseaseUpload({ onSelect, analyzing }: DiseaseUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [preview, setPreview] = useState<string | null>(null);

  const handleFile = (file: File | undefined) => {
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    onSelect(file);
  };

  return (
    <div className="rounded-3xl border-2 border-dashed border-slate-200 bg-white p-8 text-center">
      {preview ? (
        <img
          src={preview}
          alt="Selected crop"
          className="mx-auto mb-4 h-56 w-56 rounded-2xl object-cover shadow-sm"
        />
      ) : (
        <div className="mx-auto mb-4 flex h-24 w-24 items-center justify-center rounded-full bg-emerald-50">
          <Camera className="h-10 w-10 text-emerald-600" />
        </div>
      )}

      <h3 className="text-lg font-semibold text-slate-900">
        Upload a photo of the affected leaf/crop
      </h3>
      <p className="mt-1 text-sm text-slate-500">
        Clear, well-lit close-up photos give the most accurate diagnosis
      </p>

      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        className="hidden"
        onChange={(e) => handleFile(e.target.files?.[0])}
      />

      <Button
        className="mt-6 rounded-xl"
        disabled={analyzing}
        onClick={() => inputRef.current?.click()}
      >
        {analyzing ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Analyzing...
          </>
        ) : (
          <>
            <Upload className="mr-2 h-4 w-4" /> {preview ? "Choose Different Photo" : "Choose Photo"}
          </>
        )}
      </Button>
    </div>
  );
}