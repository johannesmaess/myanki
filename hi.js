import fetch from 'node-fetch';

async function invoke(action, params = {}, version = 6) {
    try {
        const body = JSON.stringify({ action, version, params })
        // console.log(body)
        const response = await fetch('http://127.0.0.1:8765', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: body
        });

        if (!response.ok) {
            throw new Error('Failed to issue request');
        }

        const data = await response.json();

        if (Object.getOwnPropertyNames(data).length !== 2) {
            throw new Error('Response has an unexpected number of fields');
        }

        if (!data.hasOwnProperty('error')) {
            throw new Error('Response is missing the required error field');
        }

        if (!data.hasOwnProperty('result')) {
            throw new Error('Response is missing the required result field');
        }

        if (data.error) {
            throw new Error(data.error);
        }

        return data.result;
    } catch (error) {
        throw error;
    }
}

// (async () => {
//     try {
//         await invoke('createDeck', 6, { deck: 'test1' });
//         const result = await invoke('deckNames', 6);
//         console.log(`Got list of decks: ${result}`);
//     } catch (error) {
//         console.error(error);
//     }
// })();



async function invokeWithDelay(method, params, delay = 100) {
    await new Promise(resolve => setTimeout(resolve, delay));
    return invoke(method, params);
}

async function main() {
    const notes = await invokeWithDelay('findNotes', {"query": "deck:Russian::A is:review prop:ease>2.5"});

    if (!Array.isArray(notes)) {
        throw new Error("findNotes did not return an array.");
    }

    console.log(`Got ${notes.length} easy notes.`);

    const result = await invokeWithDelay('notesInfo', {"notes": notes });
    // const wordsArray = result.map(item => item.fields.Word.value);
    const wordsArray = result.map((item, index) => `${index}: ${item.fields.Word.value}`);

    console.log(wordsArray.join(", "));
}

main();




