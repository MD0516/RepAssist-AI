import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  viewMode: "form",

  activeInteraction: null,

  interactionList: [],

  loading: false,

  lastUpdated: null,
};

const interactionSlice = createSlice({
  name: "interaction",

  initialState,

  reducers: {
    setActiveInteraction: (state, action) => {
      state.activeInteraction = action.payload;
      state.lastUpdated = new Date().toISOString();
    },

    setInteractionList: (state, action) => {
      state.interactionList = action.payload;
    },

    setViewMode: (state, action) => {
      state.viewMode = action.payload;
    },

    clearInteractionList: (state) => {
      state.interactionList = [];
    },

    setInteractionLoading: (state, action) => {
      state.loading = action.payload;
    },
  }
});

export const {
  setActiveInteraction,
  setInteractionList,
  setViewMode,
  clearInteractionList,
  setInteractionLoading,
} = interactionSlice.actions;

export default interactionSlice.reducer;