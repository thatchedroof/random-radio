<script lang="ts">
  import { onMount } from "svelte";
  import data from "$lib/other_rock_show.json";

  let iframeElement: HTMLIFrameElement;
  let loaded = $state(false);
  let widget: any;
  let shows = $state<typeof data>([]);
  let times = $state<number[]>([]);
  let index = $state(0);
  let first = "";

  function start() {
    const randomIndex = Math.floor(Math.random() * data.length);
    shows.push(data[randomIndex]);

    let duration = shows[index]["audio_length"];
    let randomTime = Math.floor(Math.random() * duration);
    times.push(randomTime);

    first = shows[index]["key"];

    loaded = true;

    const script = document.createElement("script");
    script.src = "//widget.mixcloud.com/media/js/widgetApi.js";
    script.type = "text/javascript";
    script.onload = () => {
      if (window.Mixcloud) {
        widget = Mixcloud.PlayerWidget(iframeElement);
        widget.ready.then(() => {
          console.log("Mixcloud widget is ready!");

          widget.events.play.on(() => {
            console.log("Mixcloud started playing!");
          });

          widget.events.pause.on(() => {
            console.log("Mixcloud paused!");
          });

          widget.events.ended.on(() => {
            widget.seek(0);
            widget.play();
          });

          load();
        });
      }
    };
    document.body.appendChild(script);
  }

  function next() {
    index = index + 1;
    if (index >= shows.length) {
      const randomIndex = Math.floor(Math.random() * data.length);
      shows.push(data[randomIndex]);

      let duration = shows[index]["audio_length"];
      let randomTime = Math.floor(Math.random() * duration);
      times.push(randomTime);
    }
    load();
  }

  function prev() {
    index = index - 1;
    if (index < 0) {
      const randomIndex = Math.floor(Math.random() * data.length);
      shows.unshift(data[randomIndex]);

      index = 0;

      let duration = shows[index]["audio_length"];
      let randomTime = Math.floor(Math.random() * duration);
      times.unshift(randomTime);
    }
    load();
  }

  async function load() {
    console.log("Loading show", shows[index]["key"]);
    console.log(widget);
    await widget.load(shows[index]["key"]);
    await widget.seek(times[index]);
  }

  function onKeyDown(event: KeyboardEvent) {
    if (event.key === "ArrowRight") {
      next();
    } else if (event.key === "ArrowLeft") {
      prev();
    }
  }
</script>

{#if loaded}
  <iframe
    width="100%"
    height="120"
    src="https://player-widget.mixcloud.com/widget/iframe/?hide_cover=1&light=1&autoplay=1&feed={encodeURIComponent(
      first,
    )}"
    frameborder="0"
    allow="autoplay"
    title="Mixcloud Player"
    bind:this={iframeElement}
  ></iframe>
{:else}
  <button onclick={start}>Load show</button>
{/if}

<svelte:window on:keydown|preventDefault={onKeyDown} />
