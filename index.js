
import * as echarts from "https://esm.sh/echarts@5.5.0";

export function render({ model, el }) {
  let container = document.createElement("div");
  
  // FORCE WIDTH/HEIGHT
  container.style.width = "100%";
  container.style.minWidth = "800px"; // <--- Add this to prevent squashing
  container.style.height = "800px";
  
  el.appendChild(container);

  let chart = echarts.init(container);

  function update() {
    let options = model.get("options");
    chart.setOption(options, { notMerge: false }); 
  }

  model.on("change:options", update);
  
  window.addEventListener("resize", () => chart.resize());
  
  // Wait a split second to ensure container is mounted in DOM before sizing
  setTimeout(() => {
     chart.resize();
  }, 100);

  update();
  
  return () => {
    chart.dispose();
  };
}

