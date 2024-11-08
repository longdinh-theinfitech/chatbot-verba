"use client";

import React, { useState } from "react";
import ChatInterface from "./ChatInterface";

import DocumentExplorer from "../Document/DocumentExplorer";

import {
  Credentials,
  RAGConfig,
  ChunkScore,
  Theme,
  DocumentFilter,
} from "@/app/types";

interface ChatViewProps {
  selectedTheme: Theme;
  credentials: Credentials;
  addStatusMessage: (
    message: string,
    type: "INFO" | "WARNING" | "SUCCESS" | "ERROR"
  ) => void;
  production: "Local" | "Demo" | "Production";
  currentPage: string;
  RAGConfig: RAGConfig | null;
  setRAGConfig: React.Dispatch<React.SetStateAction<RAGConfig | null>>;
  documentFilter: DocumentFilter[];
  setDocumentFilter: React.Dispatch<React.SetStateAction<DocumentFilter[]>>;
}

const ChatView: React.FC<ChatViewProps> = ({
  credentials,
  selectedTheme,
  addStatusMessage,
  production,
  currentPage,
  RAGConfig,
  setRAGConfig,
  documentFilter,
  setDocumentFilter,
}) => {
  const [selectedDocument, setSelectedDocument] = useState<string | null>(null);
  const [selectedChunkScore, setSelectedChunkScore] = useState<ChunkScore[]>(
    []
  );
  return (
    <div className="flex md:flex-row flex-col justify-center gap-3 h-[60vh] md:h-[80vh] ">
      <div
        className="md:flex xs:w-[45vw] w-[85%]"
      >
        <ChatInterface
          addStatusMessage={addStatusMessage}
          production={production}
          credentials={credentials}
          selectedTheme={selectedTheme}
          setSelectedDocument={setSelectedDocument}
          setSelectedChunkScore={setSelectedChunkScore}
          currentPage={currentPage}
          RAGConfig={RAGConfig}
          setRAGConfig={setRAGConfig}
          documentFilter={documentFilter}
          setDocumentFilter={setDocumentFilter}
        />
      </div>
    </div>
  );
};

export default ChatView;
