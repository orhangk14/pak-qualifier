exports.handler = async function(event, context) {
    const API_KEY = process.env.CRICAPI_KEY;
    const MATCH_ID = 'ae421629-648d-4db0-8289-5f2b950c3982';

    const url = `https://api.cricapi.com/v1/match_info?apikey=${API_KEY}&id=${MATCH_ID}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        return {
            statusCode: 200,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            body: JSON.stringify(data)
        };
    } catch (err) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Failed to fetch score' })
        };
    }
};