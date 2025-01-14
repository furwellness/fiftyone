import { debounce, merge } from "lodash";
import { useCallback, useEffect, useMemo } from "react";

import { usePanelState, useSetCustomPanelState } from "@fiftyone/spaces";
import {
  PANEL_STATE_CHANGE_DEBOUNCE,
  PANEL_STATE_PATH_CHANGE_DEBOUNCE,
} from "./constants";
import { executeOperator } from "./operators";
import { useGlobalExecutionContext } from "./state";
import usePanelEvent from "./usePanelEvent";
import { memoizedDebounce } from "./utils";
import { useUnboundState } from "@fiftyone/state";

export interface CustomPanelProps {
  panelId: string;
  onLoad?: string;
  onChange?: string;
  onUnLoad?: string;
  onChangeCtx?: string;
  onViewChange?: string;
  onChangeView?: string;
  onChangeDataset?: string;
  onChangeCurrentSample?: string;
  onChangeSelected?: string;
  onChangeSelectedLabels?: string;
  onChangeExtendedSelection?: string;
  dimensions: {
    bounds: {
      height?: number;
      width?: number;
    };
    widthRef: React.MutableRefObject<HTMLDivElement | null>;
  } | null;
  panelName?: string;
  panelLabel?: string;
}

export interface CustomPanelHooks {
  handlePanelStateChange: (state: unknown) => unknown;
  handlePanelStatePathChange: (
    path: string,
    value: unknown,
    schema: unknown,
    state?: unknown
  ) => void;
  data: unknown;
  panelSchema: unknown;
  loaded: boolean;
  onLoadError?: string;
}

function useCtxChangePanelEvent(loaded, panelId, value, operator) {
  const triggerCtxChangedEvent = usePanelEvent();
  useEffect(() => {
    if (loaded && operator) {
      triggerCtxChangedEvent(panelId, { operator, params: { value } });
    }
  }, [value, operator]);
}

export function useCustomPanelHooks(props: CustomPanelProps): CustomPanelHooks {
  const { panelId } = props;
  const [panelState] = usePanelState(null, panelId);
  const [panelStateLocal, setPanelStateLocal] = usePanelState(
    null,
    panelId,
    true
  );
  const setCustomPanelState = useSetCustomPanelState();
  const data = getPanelViewData({
    state: panelState?.state,
    data: panelStateLocal?.data,
  });
  const panelSchema = panelStateLocal?.schema;
  const ctx = useGlobalExecutionContext();
  const isLoaded: boolean = useMemo(() => {
    return panelStateLocal?.loaded;
  }, [panelStateLocal?.loaded]);
  const triggerPanelEvent = usePanelEvent();
  const lazyState = useUnboundState({ panelState });

  const onLoad = useCallback(() => {
    if (props.onLoad && !isLoaded) {
      executeOperator(
        props.onLoad,
        { panel_id: panelId, panel_state: panelState?.state },
        {
          callback(result) {
            const { error: onLoadError } = result;
            setPanelStateLocal((s) => ({ ...s, onLoadError, loaded: true }));
          },
        }
      );
    }
  }, [props.onLoad, panelId, panelState?.state, isLoaded, setPanelStateLocal]);
  useCtxChangePanelEvent(
    isLoaded,
    panelId,
    ctx._currentContext,
    props.onChangeCtx
  );
  useCtxChangePanelEvent(isLoaded, panelId, ctx.view, props.onChangeView);
  useCtxChangePanelEvent(isLoaded, panelId, ctx.viewName, props.onChangeView);
  useCtxChangePanelEvent(isLoaded, panelId, ctx.filters, props.onChangeView);
  useCtxChangePanelEvent(isLoaded, panelId, ctx.extended, props.onChangeView);
  useCtxChangePanelEvent(
    isLoaded,
    panelId,
    ctx.datasetName,
    props.onChangeDataset
  );
  useCtxChangePanelEvent(
    isLoaded,
    panelId,
    ctx.extendedSelection,
    props.onChangeExtendedSelection
  );
  useCtxChangePanelEvent(
    isLoaded,
    panelId,
    ctx.currentSample,
    props.onChangeCurrentSample
  );
  useCtxChangePanelEvent(
    isLoaded,
    panelId,
    ctx.selectedSamples,
    props.onChangeSelected
  );
  useCtxChangePanelEvent(
    isLoaded,
    panelId,
    ctx.selectedLabels,
    props.onChangeSelectedLabels
  );

  useEffect(() => {
    onLoad();
  }, [
    panelId,
    onLoad,
    props.onUnLoad,
    isLoaded,
    setPanelStateLocal,
    triggerPanelEvent,
  ]);

  useEffect(() => {
    return () => {
      if (props.onUnLoad) {
        triggerPanelEvent(panelId, { operator: props.onUnLoad });
      }
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const handlePanelStateChangeOpDebounced = useMemo(() => {
    return debounce(
      (state, onChange, panelId) => {
        if (onChange && state) {
          triggerPanelEvent(panelId, { operator: onChange });
        }
      },
      PANEL_STATE_CHANGE_DEBOUNCE,
      { leading: true }
    );
  }, [triggerPanelEvent]);

  useEffect(() => {
    handlePanelStateChangeOpDebounced(
      panelState?.state,
      props.onChange,
      panelId
    );
  }, [
    panelState?.state,
    props.onChange,
    panelId,
    handlePanelStateChangeOpDebounced,
  ]);

  const handlePanelStateChange = (newState) => {
    setCustomPanelState((state: any) => {
      return merge({}, state, newState);
    });
  };

  const handlePanelStatePathChange = useMemo(() => {
    return (path, value, schema, state) => {
      if (schema?.onChange) {
        const { panelState } = lazyState;
        const currentPanelState = merge({}, panelState?.state, state);
        triggerPanelEvent(panelId, {
          operator: schema.onChange,
          params: { path, value },
          currentPanelState,
        });
      }
    };
  }, [panelId, triggerPanelEvent, lazyState]);

  const handlePanelStatePathChangeDebounced = useMemo(() => {
    return memoizedDebounce(
      handlePanelStatePathChange,
      PANEL_STATE_PATH_CHANGE_DEBOUNCE
    );
  }, [handlePanelStatePathChange]);

  return {
    loaded: isLoaded,
    handlePanelStateChange,
    handlePanelStatePathChange: handlePanelStatePathChangeDebounced,
    data,
    panelSchema,
    onLoadError: panelStateLocal?.onLoadError,
  };
}

function getPanelViewData(panelState) {
  const state = panelState?.state;
  const data = panelState?.data;
  return merge({}, { ...state }, { ...data });
}
