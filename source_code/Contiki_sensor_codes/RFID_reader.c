#include "contiki.h"
#include "httpd-simple.h"
#include <stdio.h>
#include <string.h>

PROCESS(web_sense_process, "Sense Web Demo");
PROCESS(webserver_nogui_process, "Web server");
PROCESS_THREAD(webserver_nogui_process, ev, data)
{
    PROCESS_BEGIN();

    httpd_init();

    while(1) {
        PROCESS_WAIT_EVENT_UNTIL(ev == tcpip_event);
        httpd_appcall(data);
    }

    PROCESS_END();
}
AUTOSTART_PROCESSES(&web_sense_process, &webserver_nogui_process);

#define HISTORY 16

// Structure to represent RFID tag data
typedef struct {
    int rssi;
    int temperature;
    int id;
    int present; // 0 for absent, 1 for present
} rfid_tag_t;

// Array to store RFID tag data
static rfid_tag_t tags[4]; // Maximum 4 tags

/*---------------------------------------------------------------------------*/
static const char *TOP = "<html><head><title>RFID Reader 1</title></head><body>\n";
static const char *BOTTOM = "</body></html>\n";
/*---------------------------------------------------------------------------*/
static char buf[1024]; // Increased buffer size to accommodate more data

static void
generate_fixed_tags_data(void)
{
    // Four fixed tags with specific IDs
    tags[0].id = 1001;
    tags[1].id = 1002;
    tags[2].id = 1003;
    tags[3].id = 1004;

    // Initially all tags are present
    int i;
    for (i = 0; i < 4; i++) {
        tags[i].present = 1;
        tags[i].temperature = (rand() % 11) + 32; // Random temperature between 32 and 42
        tags[i].rssi = (rand() % 46) + 50; // Random RSSI between 50 and 95
    }
}

static void
generate_html(void)
{
    int i;
    sprintf(buf, "%s", TOP);
    for (i = 0; i < 4; i++) {
        if (tags[i].present) { // Tag is present
            sprintf(buf + strlen(buf), "<h1>Tag %d</h1>\n", i + 1);
            sprintf(buf + strlen(buf), "<p>Tag ID: %d</p>\n", tags[i].id);
            sprintf(buf + strlen(buf), "<p>Temperature: %d&deg;C</p>\n", tags[i].temperature);
            sprintf(buf + strlen(buf), "<p>RSSI: %d dBm</p>\n", tags[i].rssi);
        } else { // Tag is not present
            sprintf(buf + strlen(buf), "<h1>Tag %d</h1>\n", i + 1);
            sprintf(buf + strlen(buf), "<p>Tag has disappeared</p>\n");
        }
    }
    sprintf(buf + strlen(buf), "%s", BOTTOM);
}

static void
simulate_tag_disappearance(void)
{
    int i;
    for (i = 0; i < 4; i++) {
        if (rand() % 10 == 0) { // 10% chance of tag disappearance
            tags[i].id = -1; // Mark the tag as absent
            tags[i].temperature = -1;
            tags[i].rssi = -1;
            tags[i].present = 0;
        }
    }
}

static void
simulate_tag_reappearance(void)
{
    int i;
    for (i = 0; i < 4; i++) {
        if (rand() % 10 == 0) { // 10% chance of tag reappearance
            tags[i].temperature = (rand() % 11) + 32; // Random temperature between 32 and 42
            tags[i].rssi = (rand() % 46) + 50; // Random RSSI between 50 and 95
            tags[i].present = 1;
        }
    }
}

/*---------------------------------------------------------------------------*/
static
PT_THREAD(send_values(struct httpd_state *s))
{
    PSOCK_BEGIN(&s->sout);

    generate_fixed_tags_data();
    simulate_tag_disappearance();
    simulate_tag_reappearance();
    generate_html();

    SEND_STRING(&s->sout, buf);

    PSOCK_END(&s->sout);
}

/*---------------------------------------------------------------------------*/
httpd_simple_script_t
httpd_simple_get_script(const char *name)
{
    return send_values;
}

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(web_sense_process, ev, data)
{
    static struct etimer timer;
    PROCESS_BEGIN();

    srand(42); // Seed the random number generator

    etimer_set(&timer, CLOCK_SECOND * 5); // Update every 5 seconds

    while(1) {
        PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
        etimer_reset(&timer);
    }

    PROCESS_END();
}
/*---------------------------------------------------------------------------*/
