import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  messages: [
    {
      id: 1,
      role: "assistant",
      content:
        "Hello! Describe your interaction with the healthcare professional and I'll log it for you.",
      timestamp: new Date().toISOString(),
    },
  ],

  loading: false,
  typing: false,
};

const chatSlice = createSlice({
  name: "chat",

  initialState,

  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },

    clearMessages: (state) => {
      state.messages = initialState.messages;
    },

    setChatLoading: (state, action) => {
      state.loading = action.payload;
    },

    setTyping: (state, action) => {
      state.typing = action.payload;
    },
  },
});

export const {
  addMessage,
  clearMessages,
  setChatLoading,
  setTyping,
} = chatSlice.actions;

export default chatSlice.reducer;