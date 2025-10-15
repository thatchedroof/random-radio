<script lang="ts">
  import { onMount } from "svelte";
  import data from "$lib/other_rock_show.json";
  import { Jumper, Moon } from "svelte-loading-spinners";

  let widget: any;
  let shows = $state<typeof data>([]);
  let times = $state<number[]>([]);
  let index = $state(0);
  let fullyLoaded = $state(false);

  function start() {
    const randomIndex = Math.floor(Math.random() * data.length);
    shows.push(data[randomIndex]);

    let duration = shows[index]["audio_length"];
    let randomTime = Math.floor(Math.random() * duration);
    times.push(randomTime);

    // Load Mixcloud Widget API script dynamically
    const script = document.createElement("script");
    script.src = "//widget.mixcloud.com/media/js/widgetApi.js";
    script.type = "text/javascript";
    script.onload = async () => {
      await load();

      if ("mediaSession" in navigator) {
        console.log("Media Session API supported!");

        navigator.mediaSession.setActionHandler("play", () => {
          console.log("Play button pressed");
          widget.play();
        });

        navigator.mediaSession.setActionHandler("pause", () => {
          console.log("Pause button pressed");
          widget.pause();
        });

        navigator.mediaSession.setActionHandler("nexttrack", () => {
          console.log("Next track button pressed");
          next();
        });

        navigator.mediaSession.setActionHandler("previoustrack", () => {
          console.log("Previous track button pressed");
          prev();
        });
      }
    };
    document.body.appendChild(script);
  }

  function next() {
    fullyLoaded = false;

    times[index] = widget.getPosition();

    index = index + 1;
    if (index >= shows.length) {
      const randomIndex = Math.floor(Math.random() * data.length);
      shows.push(data[randomIndex]);

      let duration = shows[index]["audio_length"];
      let randomTime = Math.floor(Math.random() * duration);
      times.push(randomTime);
    }
  }

  function prev() {
    fullyLoaded = false;

    times[index] = widget.getPosition();

    index = index - 1;
    if (index < 0) {
      const randomIndex = Math.floor(Math.random() * data.length);
      shows.unshift(data[randomIndex]);

      index = 0;

      let duration = shows[index]["audio_length"];
      let randomTime = Math.floor(Math.random() * duration);
      times.unshift(randomTime);
    }
  }

  async function load(event: Event) {
    const iframeElement = event?.target || document.querySelector("iframe");
    if (window.Mixcloud) {
      widget = Mixcloud.PlayerWidget(iframeElement);
      await widget.ready;

      console.log("Mixcloud widget is ready!");

      widget.events.play.on(() => {
        console.log("Mixcloud started playing!");
      });

      widget.events.pause.on(() => {
        console.log("Mixcloud paused!");
      });

      widget.events.ended.on(async () => {
        await widget.seek(times[index]);
        await widget.play();
      });

      setTimeout(async () => {
        await widget.seek(times[index]);
      }, 2000);

      fullyLoaded = true;
    }
  }

  function onKeyDown(event: KeyboardEvent) {
    if (event.key === "ArrowRight" || event.key === " ") {
      next();
    } else if (event.key === "ArrowLeft") {
      prev();
    }
  }
</script>

{#if shows[index]}
  <div class="container">
    {#if !fullyLoaded}
      <div class="button-container" style="grid-row: 1 / 4;">
        <Moon size="60" color="#FF3E00" unit="px" duration="1s" />
      </div>
    {/if}
    <iframe
      width="100%"
      height="120"
      src="https://player-widget.mixcloud.com/widget/iframe/?hide_cover=1&light=1&autoplay=1&feed={encodeURIComponent(
        shows[index]['key'],
      )}"
      frameborder="0"
      allow="autoplay"
      title="Mixcloud Player"
      onload={load}
      style:display={fullyLoaded ? "block" : "none"}
    ></iframe>
    {#if fullyLoaded}
      {#if shows[index].page}
        <div
          class="song-container"
          style:display={fullyLoaded ? "block" : "none"}
        >
          {#each shows[index]?.page.song_titles as { artist, title, link }}
            <div
              class="entry"
              class:linked-entry={link}
              onclick={() => window.open(link, "_blank")}
            >
              <div class="left">{artist}</div>
              {#if title}
                <div class="dots"></div>
                <div class="right">{title}</div>
              {/if}
            </div>
          {/each}
        </div>
      {:else}
        <div class="song-container"></div>
      {/if}
      <div class="button-container">
        <button class="button prev-button" onclick={prev}>Previous</button>
        <button class="button next-button" onclick={next}>Next</button>
      </div>
    {/if}
  </div>
{:else}
  <div class="load-button-container">
    <button id="load-button" onclick={start}>Load show</button>
  </div>
{/if}

<svelte:window on:keydown|preventDefault={onKeyDown} />

<style>
  :global(body) {
    margin: 0;
    font-family: "Gentium Plus", Georgia, "Times New Roman", Times, serif;
  }

  .container {
    display: grid;
    grid-template-rows: auto auto 15%;
    height: 100vh;
    width: 100vw;
  }

  .button-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
  }

  .button {
    width: 50%;
    height: 100%;
    padding: 1rem;
    font-size: 1rem;
    color: white;
  }

  .prev-button {
    background-color: #f00;
  }

  .next-button {
    background-color: rgb(1, 155, 1);
  }

  .load-button {
    width: 100%;
    height: 100%;
    padding: 1rem;
    font-size: 1rem;
    background-color: #f00;
  }

  .load-button-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100vw;
  }

  .entry {
    display: flex;
    width: 100%;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
  }

  .linked-entry {
    cursor: pointer;
  }

  .linked-entry:hover {
    background-color: #f0f0f0;
  }

  .dots {
    max-width: 40em;
    padding: 0;
    overflow-x: hidden;
    list-style: none;
  }
  .dots li:before {
    float: left;
    width: 0;
    white-space: nowrap;
    content: ". . . . . . . . . . . . . . . . . . . . "
      ". . . . . . . . . . . . . . . . . . . . "
      ". . . . . . . . . . . . . . . . . . . . "
      ". . . . . . . . . . . . . . . . . . . . ";
  }
  .dots span:first-child {
    padding-right: 0.33em;
    background: white;
  }
  .dots span + span {
    float: right;
    padding-left: 0.33em;
    background: white;
  }

  .song-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 75vw;
    padding: 1rem;
    height: 100%;
    overflow-y: scroll;
  }
</style>
