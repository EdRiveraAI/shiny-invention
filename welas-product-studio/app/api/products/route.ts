import {NextResponse} from 'next/server';
import {store} from '../../../lib/store';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const MAX_PAYLOAD = 1_000_000;

export function GET() {
  try {
    return NextResponse.json(store().list());
  } catch {
    return NextResponse.json({error: 'Saved products could not be loaded.'}, {status: 500});
  }
}

export async function POST(request: Request) {
  let body: any;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({error: 'The product could not be read. Please try again.'}, {status: 400});
  }
  const {id, payload, revision} = body ?? {};
  if (typeof id !== 'string' || !id || id.length > 200 || typeof payload !== 'string' || !Number.isInteger(revision) || revision < 0)
    return NextResponse.json({error: 'The product could not be saved because the request was incomplete.'}, {status: 400});
  if (payload.length > MAX_PAYLOAD)
    return NextResponse.json({error: 'This product is too large to save. Shorten the notes or copy and try again.'}, {status: 413});
  try {
    // A record missing these lists would crash the page for every later visit, so refuse it here.
    const product = JSON.parse(payload);
    if (product?.id !== id || typeof product.title !== 'string' || !['stage', 'deliverables', 'listings', 'qc', 'launch'].every(k => Array.isArray(product[k]))) throw Error();
  } catch {
    return NextResponse.json({error: 'The product could not be saved because its data was malformed.'}, {status: 400});
  }
  try {
    const result = store().save(id, payload, revision);
    return result.ok ? NextResponse.json({revision: result.revision}) : NextResponse.json({error: result.error}, {status: 409});
  } catch {
    return NextResponse.json({error: 'The product could not be saved. Please try again.'}, {status: 500});
  }
}
